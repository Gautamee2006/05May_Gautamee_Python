from django.test import TestCase
from django.contrib.auth.models import User
from restaurants.models import Location, Cuisine, Restaurant
from menu.models import MenuCategory, FoodItem
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from datetime import time

class RestaurantSystemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        self.location = Location.objects.create(name='Rajkot', state='Gujarat')
        self.cuisine = Cuisine.objects.create(name='Italian', icon='fa-pizza-slice')
        
        self.restaurant = Restaurant.objects.create(
            name='Test Pizza Place',
            cuisine=self.cuisine,
            location=self.location,
            address='123 Main St',
            phone='9876543210',
            description='Best pizzas',
            rating=4.5,
            price_range='$$',
            opening_time=time(9, 0),
            closing_time=time(23, 0),
            image='https://example.com/pizza.jpg'
        )

        self.category = MenuCategory.objects.create(restaurant=self.restaurant, name='Pizzas', order=1)
        self.food_item = FoodItem.objects.create(
            restaurant=self.restaurant,
            category=self.category,
            name='Margherita Pizza',
            price=299.00,
            is_vegetarian=True
        )

    def test_restaurant_open_status(self):
        self.assertTrue(self.restaurant.is_active)
        self.assertEqual(self.restaurant.location.name, 'Rajkot')

    def test_cart_subtotal_and_total(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, food_item=self.food_item, quantity=2)
        
        self.assertEqual(cart.subtotal, 598.00)
        self.assertEqual(cart.delivery_fee, 40.00)
        self.assertEqual(cart.total, 638.00)

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            order_number='ORD-TEST1234',
            total_amount=598.00,
            discount_amount=0.00,
            final_amount=638.00,
            delivery_address='Test Address',
            phone='9876543210'
        )
        OrderItem.objects.create(
            order=order,
            food_item=self.food_item,
            food_name=self.food_item.name,
            quantity=2,
            price=299.00,
            subtotal=598.00
        )
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.status, 'pending')
