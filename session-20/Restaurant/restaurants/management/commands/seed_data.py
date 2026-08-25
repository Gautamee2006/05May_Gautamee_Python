from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from restaurants.models import Location, Cuisine, Restaurant
from menu.models import MenuCategory, FoodItem
from offers.models import Offer
from reviews.models import Review
from datetime import time, date, timedelta

class Command(BaseCommand):
    help = "Seeds initial database with locations, cuisines, restaurants, menus, offers, users, and reviews."

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Superuser & Standard Users
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@restaurant.com', 'admin123')
            admin_user.first_name = "System"
            admin_user.last_name = "Admin"
            admin_user.save()
            self.stdout.write("Created admin user: admin / admin123")

        user, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            profile = user.profile
            profile.mobile = '9876543210'
            profile.address = '102 Royal Palm Residency, Kalawad Road'
            profile.city = 'Rajkot'
            profile.save()
            self.stdout.write("Created test user: john_doe / password123")

        # 2. Locations
        locations_data = [
            {'name': 'Rajkot', 'state': 'Gujarat'},
            {'name': 'Ahmedabad', 'state': 'Gujarat'},
            {'name': 'Surat', 'state': 'Gujarat'},
            {'name': 'Vadodara', 'state': 'Gujarat'},
            {'name': 'Mumbai', 'state': 'Maharashtra'},
            {'name': 'Delhi', 'state': 'Delhi'},
        ]
        location_objs = {}
        for loc in locations_data:
            obj, _ = Location.objects.get_or_create(name=loc['name'], defaults={'state': loc['state']})
            location_objs[loc['name']] = obj

        # 3. Cuisines
        cuisines_data = [
            {
                'name': 'Gujarati',
                'icon': 'fa-utensils',
                'image': 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=600&auto=format&fit=crop&q=80',
                'description': 'Traditional authentic thali, dhokla, and sweet & savory flavors.'
            },
            {
                'name': 'Punjabi',
                'icon': 'fa-bowl-food',
                'image': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600&auto=format&fit=crop&q=80',
                'description': 'Rich butter chicken, paneer tikka, and hot garlic naans.'
            },
            {
                'name': 'Chinese',
                'icon': 'fa-cloud-meatball',
                'image': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=600&auto=format&fit=crop&q=80',
                'description': 'Flavorful noodles, fried rice, manchurian, and dim sums.'
            },
            {
                'name': 'Italian',
                'icon': 'fa-pizza-slice',
                'image': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&auto=format&fit=crop&q=80',
                'description': 'Wood-fired pizzas, creamy Alfredo pasta, and risotto.'
            },
            {
                'name': 'South Indian',
                'icon': 'fa-stroopwafel',
                'image': 'https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?w=600&auto=format&fit=crop&q=80',
                'description': 'Crispy dosas, fluffy idlis, vada, and authentic filter coffee.'
            },
            {
                'name': 'Fast Food',
                'icon': 'fa-burger',
                'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&auto=format&fit=crop&q=80',
                'description': 'Gourmet burgers, loaded fries, wraps, and crispy wings.'
            },
            {
                'name': 'Mexican',
                'icon': 'fa-pepper-hot',
                'image': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&auto=format&fit=crop&q=80',
                'description': 'Cheesy quesadillas, loaded nachos, and spicy tacos.'
            },
            {
                'name': 'Desserts',
                'icon': 'fa-ice-cream',
                'image': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=600&auto=format&fit=crop&q=80',
                'description': 'Decadent chocolate brownies, artisanal ice creams, and cakes.'
            },
        ]
        cuisine_objs = {}
        for c in cuisines_data:
            obj, _ = Cuisine.objects.get_or_create(
                name=c['name'],
                defaults={'icon': c['icon'], 'image': c['image'], 'description': c['description']}
            )
            cuisine_objs[c['name']] = obj

        # 4. Restaurants
        restaurants_data = [
            {
                'name': 'Saffron Heritage Thali',
                'cuisine': cuisine_objs['Gujarati'],
                'location': location_objs['Rajkot'],
                'address': 'Ring Road, Near Crystal Mall, Rajkot',
                'phone': '+91 98250 11223',
                'email': 'contact@saffronheritage.com',
                'description': 'Experience royal authentic Gujarati thali with over 22 traditional delicacies prepared fresh daily with ghee and love.',
                'rating': 4.8,
                'total_reviews': 124,
                'price_range': '$$',
                'opening_time': time(11, 0),
                'closing_time': time(23, 0),
                'image': 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Grand Punjabi Dhaba & Grill',
                'cuisine': cuisine_objs['Punjabi'],
                'location': location_objs['Rajkot'],
                'address': '150 Feet Ring Road, Opposite Reliance Mall, Rajkot',
                'phone': '+91 98980 44556',
                'email': 'info@grandpunjabidhaba.com',
                'description': 'Rich North Indian curries, tandoori sizzlers, and butter-dripping garlic naans in a lively rustic ambiance.',
                'rating': 4.6,
                'total_reviews': 98,
                'price_range': '$$',
                'opening_time': time(12, 0),
                'closing_time': time(23, 30),
                'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Bella Italia Bistro',
                'cuisine': cuisine_objs['Italian'],
                'location': location_objs['Ahmedabad'],
                'address': 'SG Highway, Bodakdev, Ahmedabad',
                'phone': '+91 97230 77889',
                'email': 'reservation@bellaitalia.com',
                'description': 'Authentic wood-fired Neapolitan pizzas, handcrafted tagliatelle, and house-special Tiramisu.',
                'rating': 4.9,
                'total_reviews': 210,
                'price_range': '$$$',
                'opening_time': time(12, 30),
                'closing_time': time(23, 0),
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Dragon Express Oriental',
                'cuisine': cuisine_objs['Chinese'],
                'location': location_objs['Surat'],
                'address': 'Dumas Road, Piplod, Surat',
                'phone': '+91 98241 33221',
                'email': 'hello@dragonexpress.in',
                'description': 'Indo-Chinese and Cantonese specialties including hot dumplings, sizzling pan-fried noodles, and spicy Schezwan bowls.',
                'rating': 4.5,
                'total_reviews': 86,
                'price_range': '$$',
                'opening_time': time(11, 30),
                'closing_time': time(22, 45),
                'image': 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Dakshin Flavors Cafe',
                'cuisine': cuisine_objs['South Indian'],
                'location': location_objs['Vadodara'],
                'address': 'Alkapuri Main Road, Vadodara',
                'phone': '+91 99090 88776',
                'email': 'orders@dakshinflavors.com',
                'description': 'Crispy Ghee Roast Paper Dosas, Mysore Bonda, and aromatic Kumbakonam Filter Coffee.',
                'rating': 4.7,
                'total_reviews': 150,
                'price_range': '$',
                'opening_time': time(8, 0),
                'closing_time': time(22, 0),
                'image': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'The Urban Burger Club',
                'cuisine': cuisine_objs['Fast Food'],
                'location': location_objs['Mumbai'],
                'address': 'Bandra West, Hill Road, Mumbai',
                'phone': '+91 98190 22110',
                'email': 'eat@urbanburger.com',
                'description': 'Smash burgers with melted cheddar, truffle mayo fries, and thick artisanal milkshakes.',
                'rating': 4.4,
                'total_reviews': 310,
                'price_range': '$$',
                'opening_time': time(11, 0),
                'closing_time': time(1, 0),
                'image': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Taco Bella Cantina',
                'cuisine': cuisine_objs['Mexican'],
                'location': location_objs['Delhi'],
                'address': 'Connaught Place, Block M, Delhi',
                'phone': '+91 98111 66554',
                'email': 'hola@tacobella.com',
                'description': 'Zesty burritos, crispy taco shells packed with chipotle salsa, guacamole, and jalapeños.',
                'rating': 4.3,
                'total_reviews': 75,
                'price_range': '$$$',
                'opening_time': time(12, 0),
                'closing_time': time(23, 0),
                'image': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Velvet & Cocoa Dessert Studio',
                'cuisine': cuisine_objs['Desserts'],
                'location': location_objs['Rajkot'],
                'address': 'Yagnik Road, Opposite Imperial Palace, Rajkot',
                'phone': '+91 97129 00112',
                'email': 'sweet@velvetcocoa.com',
                'description': 'Handcrafted Belgian waffles, warm molten lava cakes, and velvety sundaes.',
                'rating': 4.9,
                'total_reviews': 180,
                'price_range': '$$',
                'opening_time': time(13, 0),
                'closing_time': time(0, 0),
                'image': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&auto=format&fit=crop&q=80'
            },
        ]

        created_restaurants = []
        for r_data in restaurants_data:
            rest, _ = Restaurant.objects.get_or_create(
                name=r_data['name'],
                defaults=r_data
            )
            created_restaurants.append(rest)

        # 5. Food Menu & Categories for each restaurant
        menu_items_map = {
            'Saffron Heritage Thali': [
                {
                    'category': 'Thali Special',
                    'items': [
                        {'name': 'Executive Royal Kathiyawadi Thali', 'price': 280, 'desc': 'Includes Sev Tameta, Ringan Bharta, Gujarati Kadhi, Phulka Rotli, Bajra Rotlo with White Butter, Khichdi, Gulab Jamun, Buttermilk.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Special Swaminarayan Jain Thali', 'price': 260, 'desc': 'No onion, no garlic traditional Gujarati feast with sweet dal and fresh shrikhand.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&auto=format&fit=crop&q=80'}
                    ]
                },
                {
                    'category': 'Farsan & Starters',
                    'items': [
                        {'name': 'Khamang Dhokla Plate', 'price': 90, 'desc': 'Soft spongy steamed gram flour dhokla tempered with mustard seeds and green chilies.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Surti Locho with Butter', 'price': 110, 'desc': 'Steamed steamed savory batter served hot with butter, spicy chutney and locho masala.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500&auto=format&fit=crop&q=80'}
                    ]
                },
                {
                    'category': 'Beverages & Sweets',
                    'items': [
                        {'name': 'Masala Chhas (Buttermilk)', 'price': 30, 'desc': 'Chilled refreshing buttermilk with roasted cumin and fresh coriander.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Kesar Mango Shrikhand (250g)', 'price': 130, 'desc': 'Strained yogurt dessert infused with saffron and authentic Alphonso mango pulp.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1579954115545-aad557634293?w=500&auto=format&fit=crop&q=80'}
                    ]
                }
            ],
            'Grand Punjabi Dhaba & Grill': [
                {
                    'category': 'Starters',
                    'items': [
                        {'name': 'Paneer Tikka Sizzler', 'price': 240, 'desc': 'Cubes of cottage cheese marinated in spiced yogurt and grilled in tandoor.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Tandoori Soya Chaap', 'price': 210, 'desc': 'Tender soya chunks marinated in Kashmiri tandoori spices.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&auto=format&fit=crop&q=80'}
                    ]
                },
                {
                    'category': 'Main Course',
                    'items': [
                        {'name': 'Paneer Butter Masala', 'price': 270, 'desc': 'Rich and creamy tomato gravy with succulent paneer cubes and butter.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Dal Makhani Special', 'price': 230, 'desc': 'Black lentils simmered overnight with butter, cream, and aromatic spices.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&auto=format&fit=crop&q=80'}
                    ]
                },
                {
                    'category': 'Breads',
                    'items': [
                        {'name': 'Butter Garlic Naan', 'price': 65, 'desc': 'Leavened tandoori bread brushed with fresh garlic and melted butter.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Amritsari Kulcha', 'price': 85, 'desc': 'Stuffed spiced potato bread cooked crisply in clay tandoor.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=500&auto=format&fit=crop&q=80'}
                    ]
                }
            ],
            'Bella Italia Bistro': [
                {
                    'category': 'Wood-fired Pizzas',
                    'items': [
                        {'name': 'Classic Margherita Pizza (12")', 'price': 390, 'desc': 'San Marzano tomato sauce, fresh mozzarella fior di latte, basil, and olive oil.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Quattro Formaggi Pizza (12")', 'price': 480, 'desc': 'Four cheese blend: Mozzarella, Gorgonzola, Parmesan, and Fontina.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&auto=format&fit=crop&q=80'}
                    ]
                },
                {
                    'category': 'Pastas & Risotto',
                    'items': [
                        {'name': 'Fettuccine Creamy Alfredo', 'price': 360, 'desc': 'Handmade fettuccine in rich Parmesan cream sauce with roasted garlic and herbs.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1621996346565-e3def6166739?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Wild Mushroom Risotto', 'price': 410, 'desc': 'Arborio rice cooked with porcini mushrooms, truffle oil, and Aged Parmesan.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?w=500&auto=format&fit=crop&q=80'}
                    ]
                }
            ],
            'The Urban Burger Club': [
                {
                    'category': 'Gourmet Burgers',
                    'items': [
                        {'name': 'Classic Double Cheese Burger', 'price': 220, 'desc': 'Dual crispy veg patty loaded with melted cheddar cheese, house burger sauce, pickles.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Spicy Chipotle Crunch Burger', 'price': 250, 'desc': 'Crispy spicy patty topped with spicy chipotle mayo, jalapeños, and lettuce.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&auto=format&fit=crop&q=80'}
                    ]
                },
                {
                    'category': 'Sides & Shakes',
                    'items': [
                        {'name': 'Loaded Truffle Fries', 'price': 160, 'desc': 'French fries tossed in truffle oil, parmesan, and herbs.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500&auto=format&fit=crop&q=80'},
                        {'name': 'Nutella Monster Milkshake', 'price': 190, 'desc': 'Thick cream milkshake with Nutella, crushed cookies, and chocolate drip.', 'is_veg': True, 'img': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=500&auto=format&fit=crop&q=80'}
                    ]
                }
            ]
        }

        for rest in created_restaurants:
            menu_data = menu_items_map.get(rest.name, [
                {
                    'category': 'Popular Items',
                    'items': [
                        {'name': f"{rest.cuisine.name} Chef Special Combo", 'price': 299, 'desc': f'Signature dish prepared specially by {rest.name} head chef.', 'is_veg': True, 'img': rest.image},
                        {'name': f"Classic {rest.cuisine.name} Delicacy", 'price': 199, 'desc': f'All-time customer favorite.', 'is_veg': True, 'img': rest.image}
                    ]
                }
            ])

            for order_idx, cat_dict in enumerate(menu_data, start=1):
                cat_obj, _ = MenuCategory.objects.get_or_create(
                    restaurant=rest,
                    name=cat_dict['category'],
                    defaults={'order': order_idx}
                )
                for item_dict in cat_dict['items']:
                    FoodItem.objects.get_or_create(
                        restaurant=rest,
                        category=cat_obj,
                        name=item_dict['name'],
                        defaults={
                            'price': item_dict['price'],
                            'description': item_dict['desc'],
                            'is_vegetarian': item_dict.get('is_veg', True),
                            'image': item_dict.get('img', rest.image),
                            'is_available': True
                        }
                    )

        # 6. Offers
        offers_data = [
            {
                'restaurant': created_restaurants[0], # Saffron
                'title': 'Flat 20% OFF on Thali',
                'description': 'Enjoy 20% discount on all thali orders using code WELCOME20',
                'discount_percentage': 20,
                'coupon_code': 'WELCOME20',
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=60),
                'is_active': True
            },
            {
                'restaurant': created_restaurants[1], # Grand Punjabi
                'title': '15% OFF North Indian Feast',
                'description': 'Get 15% discount on orders above $300',
                'discount_percentage': 15,
                'coupon_code': 'TASTY15',
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=45),
                'is_active': True
            },
            {
                'restaurant': created_restaurants[2], # Bella Italia
                'title': 'Flat 25% OFF Italian Combo',
                'description': 'Special weekend offer on pizzas and pastas',
                'discount_percentage': 25,
                'coupon_code': 'FESTIVE25',
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=30),
                'is_active': True
            },
            {
                'restaurant': None, # Site-wide offer
                'title': 'Super Foodie Offer 10% OFF',
                'description': 'Applicable on any restaurant order with code FOODIE10',
                'discount_percentage': 10,
                'coupon_code': 'FOODIE10',
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=90),
                'is_active': True
            }
        ]
        for off in offers_data:
            Offer.objects.get_or_create(coupon_code=off['coupon_code'], defaults=off)

        # 7. Reviews
        if user:
            Review.objects.get_or_create(
                user=user,
                restaurant=created_restaurants[0],
                defaults={
                    'rating': 5,
                    'comment': 'Absolutely divine Gujarati Thali! The Shrikhand and Sev Tameta were out of this world. Highly recommended!'
                }
            )
            Review.objects.get_or_create(
                user=user,
                restaurant=created_restaurants[2],
                defaults={
                    'rating': 5,
                    'comment': 'Authentic wood-fired pizza with ultra crisp crust. Atmosphere is romantic and warm.'
                }
            )

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with restaurants, menus, offers, and sample user data!"))
