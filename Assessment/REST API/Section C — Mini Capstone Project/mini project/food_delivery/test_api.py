import sys
import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from food_api.models import Category, MenuItem, Order


def run_tests():
    print("==========================================")
    print("RUNNING API VERIFICATION TESTS")
    print("==========================================")

    client = APIClient()

    # 1. Test GET Categories
    response = client.get('/api/categories/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("[PASS] GET /api/categories/ (200 OK)")

    # 2. Test POST Category & Validation
    res_post_cat = client.post('/api/categories/', {'name': 'Desserts', 'description': 'Sweet items'}, format='json')
    assert res_post_cat.status_code == 201, f"Expected 201, got {res_post_cat.status_code}"
    print("[PASS] POST /api/categories/ (201 Created)")

    res_err_cat = client.post('/api/categories/', {'name': '   ', 'description': 'Empty name'}, format='json')
    assert res_err_cat.status_code == 400, f"Expected 400, got {res_err_cat.status_code}"
    assert "Category name cannot be empty." in str(res_err_cat.data), f"Unexpected message: {res_err_cat.data}"
    print("[PASS] Category empty name validation (400 Bad Request)")

    # 3. Test GET Menu Items
    response = client.get('/api/menu-items/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("[PASS] GET /api/menu-items/ (200 OK)")

    # 4. Test MenuItem Validation (price <= 0)
    cat = Category.objects.first()
    res_invalid_price = client.post('/api/menu-items/', {
        'name': 'Test Pizza',
        'price': 0,
        'category': cat.id,
        'is_available': True
    }, format='json')
    assert res_invalid_price.status_code == 400, f"Expected 400, got {res_invalid_price.status_code}"
    assert "Price must be greater than 0." in str(res_invalid_price.data), f"Unexpected message: {res_invalid_price.data}"
    print("[PASS] MenuItem price <= 0 validation (400 Bad Request)")

    # 5. Test Unauthenticated Order Creation (401 Unauthorized)
    res_unauth_order = client.post('/api/orders/', {
        'item': 'Pizza',
        'quantity': 1,
        'status': 'pending'
    }, format='json')
    assert res_unauth_order.status_code == 401, f"Expected 401, got {res_unauth_order.status_code}"
    print("[PASS] Unauthenticated POST /api/orders/ (401 Unauthorized)")

    # 6. Test Token Authentication Endpoint
    res_token = client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
    assert res_token.status_code == 200, f"Expected 200, got {res_token.status_code}"
    token_key = res_token.data['token']
    assert token_key, "Token missing in response"
    print(f"[PASS] POST /api-token-auth/ (Token: {token_key})")

    authed_client = APIClient()
    authed_client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)

    # 7. Test Authenticated Order Validation (quantity < 1)
    res_invalid_qty = authed_client.post('/api/orders/', {
        'item': 'Pizza',
        'quantity': 0,
        'status': 'pending'
    }, format='json')
    assert res_invalid_qty.status_code == 400, f"Expected 400, got {res_invalid_qty.status_code}"
    assert "Quantity must be at least 1." in str(res_invalid_qty.data), f"Unexpected message: {res_invalid_qty.data}"
    print("[PASS] Order quantity < 1 validation (400 Bad Request)")

    # 8. Test GET Orders & Pagination (PAGE_SIZE = 5)
    res_orders_p1 = client.get('/api/orders/')
    assert res_orders_p1.status_code == 200
    data_p1 = res_orders_p1.json()
    assert 'count' in data_p1
    assert data_p1['count'] >= 8, f"Expected at least 8 orders, got {data_p1['count']}"
    assert len(data_p1['results']) == 5, f"Expected page size 5, got {len(data_p1['results'])}"
    print("[PASS] GET /api/orders/ Pagination Page 1 (PAGE_SIZE = 5)")

    res_orders_p2 = client.get('/api/orders/?page=2')
    assert res_orders_p2.status_code == 200
    data_p2 = res_orders_p2.json()
    assert len(data_p2['results']) >= 3
    print("[PASS] GET /api/orders/?page=2 Pagination Page 2")

    # 9. Test Order Status Filtering
    res_filtered = client.get('/api/orders/?status=pending')
    assert res_filtered.status_code == 200
    filtered_data = res_filtered.json()
    for o in filtered_data['results']:
        assert o['status'] == 'pending', f"Expected status pending, got {o['status']}"
    print("[PASS] Order status filtering (?status=pending)")

    # 10. Test Authenticated Order Creation
    res_create_order = authed_client.post('/api/orders/', {
        'item': 'Cheese Burger',
        'quantity': 2,
        'status': 'pending'
    }, format='json')
    assert res_create_order.status_code == 201, f"Expected 201, got {res_create_order.status_code}"
    created_order = res_create_order.json()
    assert created_order['customer'] == 'testuser', f"Customer should be testuser, got {created_order['customer']}"
    print("[PASS] Authenticated POST /api/orders/ (Customer auto-assigned to testuser)")

    # 11. Test My Orders API (Authenticated)
    res_my_orders = authed_client.get('/api/my-orders/')
    assert res_my_orders.status_code == 200, f"Expected 200, got {res_my_orders.status_code}"
    my_orders_data = res_my_orders.json()
    results = my_orders_data['results'] if 'results' in my_orders_data else my_orders_data
    for item in results:
        assert item['customer'] == 'testuser', f"Order customer mismatch: {item['customer']}"
    print("[PASS] GET /api/my-orders/ (Returns only testuser's orders)")

    # 12. Test Unauthenticated Access to My Orders
    unauthed_client = APIClient()
    res_unauthed = unauthed_client.get('/api/my-orders/')
    assert res_unauthed.status_code == 401, f"Expected 401, got {res_unauthed.status_code}"
    print("[PASS] GET /api/my-orders/ Unauthenticated (401 Unauthorized)")

    print("==========================================")
    print("ALL API VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==========================================")


if __name__ == '__main__':
    run_tests()
