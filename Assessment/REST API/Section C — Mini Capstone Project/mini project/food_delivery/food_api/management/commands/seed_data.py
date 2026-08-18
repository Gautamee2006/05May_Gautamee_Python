from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from food_api.models import Category, MenuItem, Order


class Command(BaseCommand):
    help = 'Seeds initial sample data into the database'

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample data...")

        # 1. Create Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('adminpassword')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created."))
        Token.objects.get_or_create(user=admin_user)

        # 2. Create Sample Users
        user1, created = User.objects.get_or_create(username='testuser')
        if created:
            user1.set_password('testpassword')
            user1.save()
            self.stdout.write(self.style.SUCCESS("User 'testuser' created."))
        token1, _ = Token.objects.get_or_create(user=user1)

        user2, created = User.objects.get_or_create(username='user2')
        if created:
            user2.set_password('testpassword2')
            user2.save()
            self.stdout.write(self.style.SUCCESS("User 'user2' created."))
        token2, _ = Token.objects.get_or_create(user=user2)

        # 3. Create Categories
        cat_pizza, _ = Category.objects.get_or_create(
            name='Pizza',
            defaults={'description': 'Delicious wood-fired and classic pizzas'}
        )
        cat_burger, _ = Category.objects.get_or_create(
            name='Burger',
            defaults={'description': 'Juicy grilled and gourmet burgers'}
        )
        cat_indian, _ = Category.objects.get_or_create(
            name='Indian',
            defaults={'description': 'Authentic traditional Indian dishes'}
        )

        # 4. Create Menu Items
        m1, _ = MenuItem.objects.get_or_create(
            name='Margherita Pizza',
            defaults={'price': 250.00, 'category': cat_pizza, 'is_available': True}
        )
        m2, _ = MenuItem.objects.get_or_create(
            name='Cheese Burger',
            defaults={'price': 150.00, 'category': cat_burger, 'is_available': True}
        )
        m3, _ = MenuItem.objects.get_or_create(
            name='Paneer Tikka',
            defaults={'price': 300.00, 'category': cat_indian, 'is_available': True}
        )

        # 5. Create Sample Orders for testing pagination and filtering
        if Order.objects.count() == 0:
            sample_orders = [
                (user1, "Margherita Pizza", 2, "pending"),
                (user1, "Cheese Burger", 1, "confirmed"),
                (user1, "Paneer Tikka", 3, "delivered"),
                (user1, "Margherita Pizza", 1, "pending"),
                (user2, "Cheese Burger", 2, "pending"),
                (user2, "Paneer Tikka", 1, "confirmed"),
                (user2, "Margherita Pizza", 4, "delivered"),
                (user2, "Cheese Burger", 3, "confirmed"),
            ]

            for customer, item_name, qty, status in sample_orders:
                Order.objects.create(
                    customer=customer,
                    item=item_name,
                    quantity=qty,
                    status=status
                )
            self.stdout.write(self.style.SUCCESS("Sample orders created."))

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
        self.stdout.write(f"testuser Token: {token1.key}")
        self.stdout.write(f"user2 Token: {token2.key}")
