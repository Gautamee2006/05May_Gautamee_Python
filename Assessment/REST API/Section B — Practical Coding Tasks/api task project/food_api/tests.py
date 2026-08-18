from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from food_api.models import Category, MenuItem, Order


class FoodDeliveryAPITests(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        # Create Categories
        self.category_pizza = Category.objects.create(name='Pizza', description='Different types of pizzas')
        self.category_burger = Category.objects.create(name='Burger', description='Different types of burgers')

        # Create Menu Items
        self.menu_item = MenuItem.objects.create(
            name='Margherita Pizza', price=12.99, category=self.category_pizza, is_available=True
        )

        # Create Orders for pagination testing (7 orders total)
        for i in range(1, 8):
            status_choice = 'pending' if i % 2 != 0 else 'confirmed'
            Order.objects.create(
                customer_name=f'Customer {i}',
                item=f'Item {i}',
                quantity=i,
                status=status_choice
            )

    # 1. GET categories
    def test_get_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.json(), list))
        self.assertGreaterEqual(len(response.json()), 2)

    # 2. GET menu items
    def test_get_menu_items(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 3. POST menu item
    def test_post_menu_item(self):
        data = {
            "name": "Cheeseburger",
            "price": "8.99",
            "category": self.category_burger.id,
            "is_available": True
        }
        response = self.client.post('/api/menu-items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 4. Price validation (invalid price <= 0)
    def test_invalid_price_menu_item(self):
        data = {
            "name": "Free Pizza",
            "price": "0.00",
            "category": self.category_pizza.id,
            "is_available": True
        }
        response = self.client.post('/api/menu-items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Price must be greater than 0.", str(response.json()))

    # 5. GET menu item by ID
    def test_get_menu_item_by_id(self):
        response = self.client.get(f'/api/menu-items/{self.menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Margherita Pizza')

    # 6. GET non-existent menu item
    def test_get_menu_item_not_found(self):
        response = self.client.get('/api/menu-items/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 7. PUT menu item
    def test_put_menu_item(self):
        data = {
            "name": "Super Margherita Pizza",
            "price": "15.99",
            "category": self.category_pizza.id,
            "is_available": True
        }
        response = self.client.put(f'/api/menu-items/{self.menu_item.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Super Margherita Pizza')

    # 8. DELETE menu item
    def test_delete_menu_item(self):
        response = self.client.delete(f'/api/menu-items/{self.menu_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # 9. GET orders (paginated, PAGE_SIZE=5)
    def test_get_orders_pagination(self):
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 7)
        self.assertEqual(len(data['results']), 5)
        self.assertIsNotNone(data['next'])

    # 10. GET orders page 2
    def test_get_orders_page_2(self):
        response = self.client.get('/api/orders/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 2)

    # 11. GET orders status filter
    def test_get_orders_status_filter(self):
        response = self.client.get('/api/orders/?status=pending')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        for order in data['results']:
            self.assertEqual(order['status'], 'pending')

    # 12. POST order via OrderViewSet
    def test_post_order(self):
        data = {
            "customer_name": "New Customer",
            "item": "Burger",
            "quantity": 1,
            "status": "pending"
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 13. PATCH order
    def test_patch_order(self):
        response = self.client.patch('/api/orders/1/', {'status': 'delivered'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'delivered')

    # 14. Token Authentication endpoint
    def test_obtain_token(self):
        response = self.client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    # 15. POST /api/my-orders/ without token (HTTP 401)
    def test_my_orders_unauthenticated(self):
        response = self.client.post('/api/my-orders/', {'item': 'Pizza', 'quantity': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json())

    # 16. POST /api/my-orders/ with token (HTTP 201)
    def test_my_orders_authenticated_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "item": "Margherita Pizza",
            "quantity": 2,
            "status": "pending"
        }
        response = self.client.post('/api/my-orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['customer'], self.user.id)

    # 17. GET /api/my-orders/ with token (returns only user's orders)
    def test_my_orders_authenticated_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # Place an order first
        self.client.post('/api/my-orders/', {"item": "Pizza", "quantity": 1}, format='json')
        
        response = self.client.get('/api/my-orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['item'], 'Pizza')
