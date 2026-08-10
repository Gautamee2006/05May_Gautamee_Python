import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'role_project.settings')
django.setup()

from django.contrib.auth.models import User, Group
from role_app.models import Order, Product, Movie, Review, Playlist
from datetime import date

print("Seeding database with test users and sample data...")

# 1. Create Superuser
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    print("Created superuser 'admin' (password: adminpass)")

# 2. Helper to create user and assign group
def create_test_user(username, password, group_name=None, is_staff=False):
    user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com', 'is_staff': is_staff})
    if created:
        user.set_password(password)
        user.save()
        print(f"Created user '{username}' (password: {password})")
    if group_name:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        print(f"Assigned user '{username}' to group '{group_name}'")
    return user

seller = create_test_user('seller1', 'pass1234', 'Seller')
buyer = create_test_user('buyer1', 'pass1234', 'Buyer')
critic = create_test_user('critic1', 'pass1234', 'MovieCritic')
fan = create_test_user('fan1', 'pass1234', 'MovieFan')
admin_role = create_test_user('admin1', 'pass1234', 'Admin', is_staff=True)
norole = create_test_user('norole1', 'pass1234')

# 3. Seed Products
p1, _ = Product.objects.get_or_create(
    name="Mechanical Keyboard RGB",
    defaults={'price': 89.99, 'description': "High-performance mechanical keyboard with custom RGB backlight switches.", 'seller': seller}
)
p2, _ = Product.objects.get_or_create(
    name="Wireless Gaming Mouse",
    defaults={'price': 49.50, 'description': "Ergonomic ultra-lightweight gaming mouse with optical sensors.", 'seller': seller}
)

# 4. Seed Orders for Buyer
Order.objects.get_or_create(
    user=buyer,
    product_name="Mechanical Keyboard RGB",
    defaults={'price': 89.99, 'status': 'Delivered'}
)
Order.objects.get_or_create(
    user=buyer,
    product_name="Wireless Gaming Mouse",
    defaults={'price': 49.50, 'status': 'Shipped'}
)

# 5. Seed Movies
m1, _ = Movie.objects.get_or_create(
    title="Inception",
    defaults={'description': "A thief who steals corporate secrets through dream-sharing technology.", 'release_date': date(2010, 7, 16)}
)
m2, _ = Movie.objects.get_or_create(
    title="Interstellar",
    defaults={'description': "A team of explorers travel through a wormhole in space to ensure humanity's survival.", 'release_date': date(2014, 11, 7)}
)

# 6. Seed Reviews
Review.objects.get_or_create(
    movie=m1,
    user=critic,
    defaults={'rating': 5, 'comment': "A cinematic masterpiece with mind-bending visuals and thrilling score!"}
)
Review.objects.get_or_create(
    movie=m2,
    user=critic,
    defaults={'rating': 5, 'comment': "Visually stunning and deeply emotional sci-fi epic."}
)

# 7. Seed Playlists
Playlist.objects.get_or_create(
    name="Top Sci-Fi Gems",
    defaults={'description': "Collection of epic sci-fi movies of the decade.", 'created_by': admin_role}
)

print("Database seeding completed successfully!")
