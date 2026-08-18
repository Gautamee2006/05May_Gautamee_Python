import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from food_api.models import Category, MenuItem, Order

def seed():
    # 1. Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
        print("Superuser 'admin' created with password 'adminpass123'")
    else:
        print("Superuser 'admin' already exists")

    # 2. Create Test User & Token
    testuser, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    if created:
        testuser.set_password('testpassword')
        testuser.save()
        token, _ = Token.objects.get_or_create(user=testuser)
        print(f"Test user 'testuser' created with password 'testpassword' and Token: {token.key}")
    else:
        token, _ = Token.objects.get_or_create(user=testuser)
        print(f"Test user 'testuser' exists with Token: {token.key}")

    # 3. Create Categories
    c1, _ = Category.objects.get_or_create(name='Pizza', defaults={'description': 'Different types of pizzas'})
    c2, _ = Category.objects.get_or_create(name='Burger', defaults={'description': 'Different types of burgers'})
    c3, _ = Category.objects.get_or_create(name='Beverages', defaults={'description': 'Refreshing drinks and beverages'})
    print("Categories seeded")

    # 4. Create Menu Items
    m1, _ = MenuItem.objects.get_or_create(name='Margherita Pizza', defaults={'price': 12.99, 'category': c1, 'is_available': True})
    m2, _ = MenuItem.objects.get_or_create(name='Pepperoni Pizza', defaults={'price': 14.99, 'category': c1, 'is_available': True})
    m3, _ = MenuItem.objects.get_or_create(name='Cheeseburger', defaults={'price': 8.99, 'category': c2, 'is_available': True})
    m4, _ = MenuItem.objects.get_or_create(name='Veggie Burger', defaults={'price': 7.99, 'category': c2, 'is_available': True})
    m5, _ = MenuItem.objects.get_or_create(name='Coca Cola', defaults={'price': 2.50, 'category': c3, 'is_available': True})
    print("Menu items seeded")

    # 5. Create Orders
    orders_data = [
        {'customer_name': 'John Doe', 'item': 'Margherita Pizza', 'quantity': 2, 'status': 'pending'},
        {'customer_name': 'Jane Smith', 'item': 'Cheeseburger', 'quantity': 1, 'status': 'confirmed'},
        {'customer_name': 'Bob Wilson', 'item': 'Pepperoni Pizza', 'quantity': 3, 'status': 'delivered'},
        {'customer_name': 'Alice Johnson', 'item': 'Veggie Burger', 'quantity': 2, 'status': 'pending'},
        {'customer_name': 'Charlie Brown', 'item': 'Coca Cola', 'quantity': 4, 'status': 'confirmed'},
        {'customer_name': 'David Miller', 'item': 'Margherita Pizza', 'quantity': 1, 'status': 'pending'},
        {'customer_name': 'Emma Davis', 'item': 'Cheeseburger', 'quantity': 2, 'status': 'delivered'},
    ]
    for o_data in orders_data:
        Order.objects.get_or_create(
            customer_name=o_data['customer_name'],
            item=o_data['item'],
            defaults={'quantity': o_data['quantity'], 'status': o_data['status']}
        )
    print("Orders seeded")

if __name__ == '__main__':
    seed()
