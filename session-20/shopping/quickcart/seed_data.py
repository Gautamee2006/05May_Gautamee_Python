import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickcart.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Profile, Address
from products.models import Category, Product, Review
from coupons.models import Coupon
from support.models import FAQ
from datetime import date, timedelta

def seed():
    print("Seeding database for QuickCart...")

    # 1. Create Admin & Demo Users
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@quickcart.com', 'admin123')
        admin.first_name = "System"
        admin.last_name = "Admin"
        admin.save()
        print("Created Superuser: admin / admin123")

    if not User.objects.filter(username='john_doe').exists():
        user = User.objects.create_user('john_doe', 'john@example.com', 'pass123')
        user.first_name = "John"
        user.last_name = "Doe"
        user.save()
        
        Address.objects.create(
            user=user,
            full_name="John Doe",
            mobile="9876543210",
            house_flat="Flat 402, Sunshine Heights",
            street="MG Road",
            area="Koramangala",
            city="Bengaluru",
            state="Karnataka",
            pincode="560034",
            address_type="Home",
            is_default=True
        )
        print("Created Demo User: john_doe / pass123")

    # 2. Create Categories
    categories_data = [
        {"name": "Electronics & Tech", "slug": "electronics-tech", "description": "Laptops, Smartphones, Headphones & Accessories"},
        {"name": "Men's Fashion", "slug": "mens-fashion", "description": "Shirts, Jeans, Jackets & Footwear"},
        {"name": "Women's Clothing", "slug": "womens-clothing", "description": "Dresses, Tops, Ethnic Wear & Handbags"},
        {"name": "Home & Kitchen", "slug": "home-kitchen", "description": "Appliances, Decor, Cookware & Furniture"},
        {"name": "Books & Stationery", "slug": "books-stationery", "description": "Bestsellers, Fiction, Self-Help & Notebooks"},
        {"name": "Beauty & Wellness", "slug": "beauty-wellness", "description": "Skincare, Haircare, Perfumes & Grooming"}
    ]

    cat_objs = {}
    for cdata in categories_data:
        cat, _ = Category.objects.get_or_create(slug=cdata["slug"], defaults=cdata)
        cat_objs[cdata["slug"]] = cat
    print(f"Created/Verified {len(cat_objs)} Categories.")

    # 3. Create Demo Products
    products_data = [
        {
            "category": cat_objs["electronics-tech"],
            "name": "UltraNoise Wireless Noise Cancelling Headphones",
            "brand": "AudioTech",
            "price": 14999.00,
            "discount_percentage": 20,
            "stock": 15,
            "sku": "AUD-WH-100",
            "description": "Experience premium sound clarity with active noise cancellation, 30-hour battery life, and ultra-soft memory foam ear cushions.",
            "rating": 4.8
        },
        {
            "category": cat_objs["electronics-tech"],
            "name": "ProBook 15.6 Inch Full HD Laptop (16GB RAM, 512GB SSD)",
            "brand": "TechCorp",
            "price": 64999.00,
            "discount_percentage": 15,
            "stock": 8,
            "sku": "TC-PB-512",
            "description": "Powerful Intel i7 processor paired with high-speed 16GB RAM and lightning-fast NVMe SSD storage.",
            "rating": 4.6
        },
        {
            "category": cat_objs["electronics-tech"],
            "name": "FitPulse Smartwatch with AMOLED Display & SpO2",
            "brand": "FitPulse",
            "price": 4999.00,
            "discount_percentage": 40,
            "stock": 25,
            "sku": "FP-SW-200",
            "description": "Track your heart rate, sleep, workouts, and receive smartphone notifications on a vibrant 1.4-inch AMOLED display.",
            "rating": 4.5
        },
        {
            "category": cat_objs["mens-fashion"],
            "name": "Classic Denim Slim Fit Jacket for Men",
            "brand": "UrbanStyle",
            "price": 3499.00,
            "discount_percentage": 30,
            "stock": 12,
            "sku": "US-DJ-01",
            "description": "Timeless indigo denim jacket crafted from 100% premium cotton with durable button closures.",
            "rating": 4.3
        },
        {
            "category": cat_objs["mens-fashion"],
            "name": "Breathable Lightweight Running Shoes",
            "brand": "SprintAir",
            "price": 2999.00,
            "discount_percentage": 25,
            "stock": 18,
            "sku": "SA-RS-99",
            "description": "Ergonomic mesh upper with shock-absorbing EVA sole for maximum comfort during long runs.",
            "rating": 4.7
        },
        {
            "category": cat_objs["womens-clothing"],
            "name": "Floral Print Summer Midi Dress",
            "brand": "BellaModa",
            "price": 2499.00,
            "discount_percentage": 35,
            "stock": 10,
            "sku": "BM-SD-44",
            "description": "Elegant floral midi dress made from lightweight chiffon fabric, perfect for casual outings and parties.",
            "rating": 4.9
        },
        {
            "category": cat_objs["home-kitchen"],
            "name": "Multi-Function Digital Air Fryer 4.2L",
            "brand": "HomeChef",
            "price": 7999.00,
            "discount_percentage": 30,
            "stock": 6,
            "sku": "HC-AF-42",
            "description": "Cook crisp and healthy fried food with 90% less oil using rapid air circulation technology.",
            "rating": 4.8
        },
        {
            "category": cat_objs["home-kitchen"],
            "name": "Stainless Steel Cookware Set (5 Pieces)",
            "brand": "KitchenPro",
            "price": 4500.00,
            "discount_percentage": 20,
            "stock": 4,
            "sku": "KP-CS-05",
            "description": "Induction-compatible triple-ply stainless steel pots and pans with heat-resistant handles.",
            "rating": 4.4
        },
        {
            "category": cat_objs["books-stationery"],
            "name": "Atomic Habits by James Clear (Hardcover)",
            "brand": "Penguin Books",
            "price": 799.00,
            "discount_percentage": 10,
            "stock": 50,
            "sku": "BK-AH-01",
            "description": "An easy and proven way to build good habits and break bad ones. Transform your daily routine.",
            "rating": 4.9
        },
        {
            "category": cat_objs["beauty-wellness"],
            "name": "Hydrating Vitamin C Face Serum (50ml)",
            "brand": "GlowNatural",
            "price": 1199.00,
            "discount_percentage": 15,
            "stock": 30,
            "sku": "GN-VS-50",
            "description": "Enriched with Pure Vitamin C and Hyaluronic Acid to brighten skin tone and boost collagen production.",
            "rating": 4.6
        }
    ]

    for pdata in products_data:
        p, created = Product.objects.get_or_create(sku=pdata["sku"], defaults=pdata)
        if created:
            print(f"Created Product: {p.name}")

    # 4. Create Coupons
    coupons = [
        {"code": "QUICK10", "discount_type": "percentage", "discount_value": 10.0, "min_order_amount": 999.0, "usage_limit": 100, "expiry_date": date.today() + timedelta(days=60)},
        {"code": "WELCOME20", "discount_type": "percentage", "discount_value": 20.0, "min_order_amount": 1499.0, "usage_limit": 50, "expiry_date": date.today() + timedelta(days=30)},
        {"code": "FESTIVE500", "discount_type": "fixed", "discount_value": 500.0, "min_order_amount": 2999.0, "usage_limit": 20, "expiry_date": date.today() + timedelta(days=15)},
    ]

    for cdata in coupons:
        Coupon.objects.get_or_create(code=cdata["code"], defaults=cdata)
    print("Created/Verified Coupons.")

    # 5. Create FAQs
    faqs = [
        {"category": "Account", "question": "How do I create a QuickCart account?", "answer": "Click on 'Register' at the top right corner, enter your details, verify your OTP, and start shopping immediately!"},
        {"category": "Orders", "question": "How can I track my order status?", "answer": "Go to 'My Orders' under your profile menu, select the order you want to track, and view the live tracking status stepper."},
        {"category": "Payments", "question": "What payment methods are supported?", "answer": "We accept Cash on Delivery (COD), UPI payments, Credit/Debit Cards, and Net Banking."},
        {"category": "Returns", "question": "What is the return policy?", "answer": "You can request a return within 7 days of delivery directly from your 'Order Details' page."},
        {"category": "Coupons", "question": "How do I apply a coupon discount?", "answer": "Enter the coupon code in the shopping cart price details section before proceeding to checkout."}
    ]

    for fdata in faqs:
        FAQ.objects.get_or_create(question=fdata["question"], defaults=fdata)
    print("Created FAQs.")

    print("\nDatabase seeding completed successfully!")

if __name__ == '__main__':
    seed()
