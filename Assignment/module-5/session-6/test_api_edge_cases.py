import requests

BASE_URL = "http://127.0.0.1:8005/api"

def test_missing_fields():
    print("=== Testing Missing Fields Validation ===")
    
    # Send email missing email field
    r1 = requests.post(f"{BASE_URL}/send-email/", json={})
    print(f"Email missing field: Status {r1.status_code}, Body: {r1.json()}")
    
    # Send SMS missing message field
    r2 = requests.post(f"{BASE_URL}/send-sms/", json={"phone_number": "+1234567890"})
    print(f"SMS missing field: Status {r2.status_code}, Body: {r2.json()}")
    
    # Pay missing amount field
    r3 = requests.post(f"{BASE_URL}/pay/", json={"currency": "usd"})
    print(f"Pay missing field: Status {r3.status_code}, Body: {r3.json()}")
    
    # Google login missing token field
    r4 = requests.post(f"{BASE_URL}/google-login/", json={})
    print(f"Google login missing field: Status {r4.status_code}, Body: {r4.json()}")

if __name__ == "__main__":
    test_missing_fields()
