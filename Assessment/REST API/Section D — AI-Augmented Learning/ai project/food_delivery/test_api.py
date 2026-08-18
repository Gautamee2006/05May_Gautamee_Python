import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from django.test import Client
from orders.models import Order

def run_tests():
    client = Client()
    print("==========================================")
    print("RUNNING API VERIFICATION TESTS")
    print("==========================================")

    # Clear existing orders for clean test state
    Order.objects.all().delete()

    # TEST 1: SUCCESSFUL REQUEST
    print("\n--- TEST 1: Valid Order Placement (quantity=2) ---")
    payload1 = {
        "customer_name": "Gautamee",
        "item": "Pizza",
        "quantity": 2
    }
    response1 = client.post('/api/orders/place/', data=json.dumps(payload1), content_type='application/json')
    print(f"Status Code: {response1.status_code}")
    print(f"Response Data: {response1.json()}")
    assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"
    res_data1 = response1.json()
    assert res_data1["id"] is not None, "Missing auto-generated ID"
    assert res_data1["customer_name"] == "Gautamee"
    assert res_data1["item"] == "Pizza"
    assert res_data1["quantity"] == 2
    print("SUCCESS: Valid order created with auto-generated id!")

    # TEST 2: VALIDATION FAILURE (quantity=0)
    print("\n--- TEST 2: Validation Failure (quantity=0) ---")
    payload2 = {
        "customer_name": "Gautamee",
        "item": "Pizza",
        "quantity": 0
    }
    response2 = client.post('/api/orders/place/', data=json.dumps(payload2), content_type='application/json')
    print(f"Status Code: {response2.status_code}")
    print(f"Response Data: {response2.json()}")
    assert response2.status_code == 400, f"Expected 400, got {response2.status_code}"
    assert "quantity" in response2.json()
    assert "Quantity must be a positive integer." in response2.json()["quantity"]
    print("SUCCESS: quantity=0 rejected with HTTP 400 and clear error message!")

    # TEST 3: VALIDATION FAILURE (quantity=-1)
    print("\n--- TEST 3: Validation Failure (quantity=-1) ---")
    payload3 = {
        "customer_name": "Gautamee",
        "item": "Pizza",
        "quantity": -1
    }
    response3 = client.post('/api/orders/place/', data=json.dumps(payload3), content_type='application/json')
    print(f"Status Code: {response3.status_code}")
    print(f"Response Data: {response3.json()}")
    assert response3.status_code == 400, f"Expected 400, got {response3.status_code}"
    assert "quantity" in response3.json()
    assert "Quantity must be a positive integer." in response3.json()["quantity"]
    print("SUCCESS: quantity=-1 rejected with HTTP 400 and clear error message!")

    # TEST 4: VALIDATION FAILURE (quantity="abc")
    print("\n--- TEST 4: Validation Failure (quantity='abc') ---")
    payload4 = {
        "customer_name": "Gautamee",
        "item": "Pizza",
        "quantity": "abc"
    }
    response4 = client.post('/api/orders/place/', data=json.dumps(payload4), content_type='application/json')
    print(f"Status Code: {response4.status_code}")
    print(f"Response Data: {response4.json()}")
    assert response4.status_code == 400, f"Expected 400, got {response4.status_code}"
    assert "quantity" in response4.json()
    print("SUCCESS: Non-integer quantity rejected with HTTP 400!")

    # TEST 5: DATABASE CHECK
    print("\n--- TEST 5: Database Persistence Check ---")
    orders_count = Order.objects.count()
    print(f"Total Orders in DB: {orders_count}")
    assert orders_count == 1, f"Expected 1 order in DB, found {orders_count}"
    saved_order = Order.objects.first()
    print(f"Saved Order in DB: {saved_order}")
    print("SUCCESS: Only valid orders were saved to database!")

    print("\n==========================================")
    print("ALL TESTS PASSED PERFECTLY!")
    print("==========================================")

if __name__ == '__main__':
    run_tests()
