import requests

BASE_URL = "http://127.0.0.1:4556/api"

def test_send_email():
    print("\n--- Testing /api/send-email/ ---")
    payload = {"email": "gatukakadiya@gmail.com"}
    response = requests.post(f"{BASE_URL}/send-email/", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

def test_send_sms():
    print("\n--- Testing /api/send-sms/ ---")
    payload = {"phone_number": "+919601933815", "message": "Welcome SMS test!"}
    response = requests.post(f"{BASE_URL}/send-sms/", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

def test_pay():
    print("\n--- Testing /api/pay/ ---")
    payload = {"amount": 1500, "currency": "usd"}
    response = requests.post(f"{BASE_URL}/pay/", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

def test_google_login():
    print("\n--- Testing /api/google-login/ ---")
    payload = {"id_token": "invalid_mock_token_for_validation"}
    response = requests.post(f"{BASE_URL}/google-login/", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

if __name__ == "__main__":
    test_send_email()
    test_send_sms()
    test_pay()
    test_google_login()
