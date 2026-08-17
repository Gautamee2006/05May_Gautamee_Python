import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodiehub.settings')
django.setup()

from rest_framework.test import APIClient
from api.views import RestaurantViewSet, StandardPageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

client = APIClient()

def get_items(response_data):
    if isinstance(response_data, dict):
        return response_data.get('results', [])
    return response_data

print("="*60)
print("TEST 1: Testing PageNumberPagination (3 items per page)")
print("="*60)
# Temporarily set pagination to PageNumberPagination (3 per page)
RestaurantViewSet.pagination_class = StandardPageNumberPagination
res = client.get('/api/restaurants/')
print(f"Status Code: {res.status_code}")
items = get_items(res.data)
print(f"Total Count in DB: {res.data.get('count')}")
print(f"Items returned on page 1: {len(items)}")
assert len(items) == 3, f"Expected 3 items per page, got {len(items)}"
print("PAGE NUMBER PAGINATION PASSED SUCCESSFULLY!\n")

print("="*60)
print("TEST 2: Testing LimitOffsetPagination (/api/restaurants/?limit=2&offset=2)")
print("="*60)
# Switch pagination to LimitOffsetPagination as requested
RestaurantViewSet.pagination_class = LimitOffsetPagination
res = client.get('/api/restaurants/?limit=2&offset=2')
print(f"Status Code: {res.status_code}")
items = get_items(res.data)
print(f"Total Count: {res.data.get('count')}")
print(f"Items returned: {len(items)}")
print("Results slice:")
for item in items:
    print(f"  ID: {item['id']}, Name: {item['name']}, Cuisine: {item['cuisine']}")
assert len(items) == 2, f"Expected 2 items, got {len(items)}"
print("LIMIT OFFSET PAGINATION PASSED SUCCESSFULLY!\n")

print("="*60)
print("TEST 3: Testing Ordering by name (/api/restaurants/?ordering=name)")
print("="*60)
res = client.get('/api/restaurants/?ordering=name')
items = get_items(res.data)
names = [r['name'] for r in items]
print(f"Ordered names: {names}")
assert names == sorted(names), "Names not sorted in ascending order!"
print("ORDERING BY NAME PASSED SUCCESSFULLY!\n")

print("="*60)
print("TEST 4: Testing Ordering by -cuisine (/api/restaurants/?ordering=-cuisine)")
print("="*60)
res = client.get('/api/restaurants/?ordering=-cuisine')
items = get_items(res.data)
cuisines = [r['cuisine'] for r in items]
print(f"Ordered cuisines (descending): {cuisines}")
assert cuisines == sorted(cuisines, reverse=True), "Cuisines not sorted in descending order!"
print("ORDERING BY -CUISINE PASSED SUCCESSFULLY!\n")

print("="*60)
print("TEST 5: Testing Filtering by cuisine (/api/restaurants/?cuisine=Italian)")
print("="*60)
res = client.get('/api/restaurants/?cuisine=Italian')
print(f"Status Code: {res.status_code}")
italian_items = get_items(res.data)
print(f"Filtered count: {len(italian_items)}")
for item in italian_items:
    print(f"  Name: {item['name']}, Cuisine: {item['cuisine']}")
    assert item['cuisine'] == 'Italian', f"Expected Italian, got {item['cuisine']}"
assert len(italian_items) == 3, f"Expected 3 Italian restaurants, got {len(italian_items)}"
print("CUISINE FILTER PASSED SUCCESSFULLY!\n")

print("="*60)
print("ALL 5 TASKS VERIFIED AND WORKING PERFECTLY!")
print("="*60)
