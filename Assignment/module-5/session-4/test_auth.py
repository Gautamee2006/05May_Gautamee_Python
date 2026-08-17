import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import base64

User = get_user_model()


def run_tests():
    print("=" * 60)
    print("RUNNING DRF AUTHENTICATION & PERMISSIONS TEST SUITE")
    print("=" * 60)

    # Clean up existing test users if any
    User.objects.filter(username__in=["basic_user", "token_user", "session_user", "premium_user", "regular_user"]).delete()

    # 1. Create Test Users
    basic_user = User.objects.create_user(username="basic_user", password="password123")
    token_user = User.objects.create_user(username="token_user", password="password123")
    session_user = User.objects.create_user(username="session_user", password="password123")
    premium_user = User.objects.create_user(username="premium_user", password="password123", is_premium=True)
    regular_user = User.objects.create_user(username="regular_user", password="password123", is_premium=False)

    # 2. Generate Auth Token for token_user
    token, _ = Token.objects.get_or_create(user=token_user)
    print(f"\n[INFO] Generated Token for '{token_user.username}': {token.key}")

    client = APIClient()

    # -------------------------------------------------------------
    # TASK 1: BasicAuthentication on /api/playlists/
    # -------------------------------------------------------------
    print("\n--- Task 1: /api/playlists/ (BasicAuthentication) ---")
    
    # Without Auth
    res_no_auth = client.get('/api/playlists/')
    print(f"Without Credentials -> Status: {res_no_auth.status_code}")
    assert res_no_auth.status_code == 401, f"Expected 401, got {res_no_auth.status_code}"

    # With Basic Auth
    auth_header = "Basic " + base64.b64encode(b"basic_user:password123").decode('ascii')
    res_auth = client.get('/api/playlists/', HTTP_AUTHORIZATION=auth_header)
    print(f"With Valid BasicAuth -> Status: {res_auth.status_code}, Response: {res_auth.data}")
    assert res_auth.status_code == 200, f"Expected 200, got {res_auth.status_code}"

    # -------------------------------------------------------------
    # TASK 2: TokenAuthentication on /api/orders/
    # -------------------------------------------------------------
    print("\n--- Task 2: /api/orders/ (TokenAuthentication) ---")
    
    # Without Token
    res_no_token = client.get('/api/orders/')
    print(f"Without Token -> Status: {res_no_token.status_code}")
    assert res_no_token.status_code == 401, f"Expected 401, got {res_no_token.status_code}"

    # With Valid Token
    res_token = client.get('/api/orders/', HTTP_AUTHORIZATION=f'Token {token.key}')
    print(f"With Valid Token -> Status: {res_token.status_code}, Response: {res_token.data}")
    assert res_token.status_code == 200, f"Expected 200, got {res_token.status_code}"

    # -------------------------------------------------------------
    # TASK 3: SessionAuthentication on /api/cart/
    # -------------------------------------------------------------
    print("\n--- Task 3: /api/cart/ (SessionAuthentication) ---")

    # Unauthenticated Request (Must receive 403 Forbidden)
    res_unauth_cart = client.post('/api/cart/', {'item': 'Laptop'})
    print(f"Unauthenticated User -> Status: {res_unauth_cart.status_code} (Expected 403 Forbidden)")
    assert res_unauth_cart.status_code == 403, f"Expected 403, got {res_unauth_cart.status_code}"

    # Authenticated Session User
    client.force_login(session_user)
    res_auth_cart = client.post('/api/cart/', {'item': 'Smartphone'})
    print(f"Logged-in Session User -> Status: {res_auth_cart.status_code}, Response: {res_auth_cart.data}")
    assert res_auth_cart.status_code == 200, f"Expected 200, got {res_auth_cart.status_code}"
    client.logout()

    # -------------------------------------------------------------
    # TASK 4: IsPremiumUser Permission on /api/tickets/
    # -------------------------------------------------------------
    print("\n--- Task 4: /api/tickets/ (IsPremiumUser Permission) ---")

    # Non-Premium User (is_premium=False)
    client.force_login(regular_user)
    res_non_premium = client.get('/api/tickets/')
    print(f"Non-Premium User (is_premium=False) -> Status: {res_non_premium.status_code} (Forbidden)")
    assert res_non_premium.status_code == 403, f"Expected 403, got {res_non_premium.status_code}"
    client.logout()

    # Premium User (is_premium=True)
    client.force_login(premium_user)
    res_premium = client.get('/api/tickets/')
    print(f"Premium User (is_premium=True) -> Status: {res_premium.status_code}, Response: {res_premium.data}")
    assert res_premium.status_code == 200, f"Expected 200, got {res_premium.status_code}"
    client.logout()

    print("\n" + "=" * 60)
    print("ALL 5 TASKS TESTED AND PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
