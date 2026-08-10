import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'role_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User, Group
from role_app.models import Order, Product, Movie, Review, Playlist
from role_app.admin import PlaylistAdmin
from django.contrib.admin.sites import AdminSite

client = Client()

print("--- Running Role-Based Auth Verification Tests ---")

# 1. Test Unauthenticated Access to /orders/ -> Redirects to /login/
res = client.get('/orders/')
assert res.status_code == 302 and '/login/' in res.url, f"Expected redirect to login, got {res.status_code}"
print("[OK] Unauthenticated /orders/ correctly redirects to /login/")

# 2. Test Buyer Access to /orders/ & /post-product/
client.login(username='buyer1', password='pass1234')
res = client.get('/orders/')
assert res.status_code == 200, f"Expected 200 for buyer /orders/, got {res.status_code}"
assert 'Mechanical Keyboard RGB' in res.content.decode(), "Buyer orders page should contain buyer's orders"
print("[OK] Buyer can access /orders/ and see their own orders")

res = client.get('/post-product/')
assert res.status_code == 403, f"Expected 403 for buyer accessing /post-product/, got {res.status_code}"
print("[OK] Buyer receives 403 Permission Denied on /post-product/")
client.logout()

# 3. Test Seller Access to /post-product/
client.login(username='seller1', password='pass1234')
res = client.get('/post-product/')
assert res.status_code == 200, f"Expected 200 for seller on /post-product/, got {res.status_code}"
print("[OK] Seller can access /post-product/")
client.logout()

# 4. Test MovieCritic vs MovieFan permissions on /reviews/add/
client.login(username='fan1', password='pass1234')
res = client.get('/reviews/add/')
assert res.status_code == 403, f"Expected 403 for fan on /reviews/add/, got {res.status_code}"
print("[OK] MovieFan receives 403 Permission Denied on /reviews/add/")
client.logout()

client.login(username='critic1', password='pass1234')
res = client.get('/reviews/add/')
assert res.status_code == 200, f"Expected 200 for critic on /reviews/add/, got {res.status_code}"
print("[OK] MovieCritic can access /reviews/add/")
client.logout()

# 5. Test Playlist Admin access
client.login(username='buyer1', password='pass1234')
res = client.get('/playlist-admin/')
assert res.status_code == 403, f"Expected 403 for non-admin on /playlist-admin/, got {res.status_code}"
print("[OK] Non-Admin group member receives 403 on /playlist-admin/")
client.logout()

client.login(username='admin1', password='pass1234')
res = client.get('/playlist-admin/')
assert res.status_code == 200, f"Expected 200 for admin group user on /playlist-admin/, got {res.status_code}"
print("[OK] Admin group member can access /playlist-admin/")
client.logout()

# 6. Test PlaylistAdmin ModelAdmin Permission Overrides
site = AdminSite()
playlist_admin = PlaylistAdmin(Playlist, site)

class DummyRequest:
    def __init__(self, user):
        self.user = user

admin_user = User.objects.get(username='admin1')
buyer_user = User.objects.get(username='buyer1')

assert playlist_admin.has_view_permission(DummyRequest(admin_user)) == True, "PlaylistAdmin should allow view for Admin group"
assert playlist_admin.has_view_permission(DummyRequest(buyer_user)) == False, "PlaylistAdmin should deny view for non-Admin group"
assert playlist_admin.has_add_permission(DummyRequest(admin_user)) == True
assert playlist_admin.has_add_permission(DummyRequest(buyer_user)) == False
print("[OK] PlaylistAdmin ModelAdmin permission overrides correctly check 'Admin' Django Group!")

# 7. Test Product Purchase by Buyer
product = Product.objects.first()
client.login(username='buyer1', password='pass1234')
res = client.post(f'/buy-product/{product.id}/')
assert res.status_code == 302 and '/orders/' in res.url, "Buy product should redirect to /orders/"
new_order = Order.objects.filter(user__username='buyer1', product_name=product.name).latest('order_date')
assert new_order is not None, "New order should be created for buyer"
print("[OK] Buyer successfully purchased product and order record was created!")
client.logout()

print("\n--- ALL ROLE-BASED AUTH TESTS PASSED SUCCESSFULLY! ---")

