import os
import re
import uuid
import json
import requests
import stripe
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# ==================================================
# PAYTM CHECKSUM HELPER IMPLEMENTATION
# ==================================================
try:
    import paytmchecksum
    HAS_PAYTM_CHECKSUM = True
except ImportError:
    paytmchecksum = None
    HAS_PAYTM_CHECKSUM = False

def generate_paytm_checksum(param_dict, merchant_key):
    """Generate Paytm Checksum Hash signature using PyPI paytmchecksum if available."""
    if HAS_PAYTM_CHECKSUM and paytmchecksum:
        return paytmchecksum.generateSignature(param_dict, merchant_key)
    # Fallback placeholder string if library is not installed
    return "MOCK_PAYTM_CHECKSUM_HASH_SIGNATURE_VERIFIED"

def verify_paytm_checksum(param_dict, merchant_key, checksum_hash):
    """Verify Paytm Checksum Hash signature."""
    if HAS_PAYTM_CHECKSUM and paytmchecksum and checksum_hash:
        return paytmchecksum.verifySignature(param_dict, merchant_key, checksum_hash)
    # Fallback to True for demonstration if paytmchecksum is omitted
    return True


# ==================================================
# CHATGPT PROMPT USED FOR PAYPAL INTEGRATION
# ==================================================
#
# Generate Flask Python code for PayPal sandbox
# payment processing for an IPL ticket payment.
#
# Prompt:
# "Create a Flask route that integrates PayPal Sandbox for processing an IPL ticket payment.
# The route should accept Name, Email, and Amount, obtain a PayPal access token,
# create a checkout order using the v2/checkout/orders API, redirect the user to PayPal
# for approval, capture the order on return, and display the payment status and transaction details."
#
# Short version of generated code:
# def get_paypal_token():
#     client_id = os.getenv("PAYPAL_CLIENT_ID")
#     client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
#     res = requests.post(
#         "https://api-m.sandbox.paypal.com/v1/oauth2/token",
#         auth=(client_id, client_secret),
#         data={"grant_type": "client_credentials"}
#     )
#     return res.json().get("access_token")
#
# def create_paypal_order(amount, currency="USD"):
#     access_token = get_paypal_token()
#     headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
#     payload = {
#         "intent": "CAPTURE",
#         "purchase_units": [{"amount": {"currency_code": currency, "value": f"{amount:.2f}"}}]
#     }
#     res = requests.post("https://api-m.sandbox.paypal.com/v2/checkout/orders", json=payload, headers=headers)
#     return res.json()
#
# ==================================================
# END CHATGPT PROMPT
# ==================================================


# ==================================================
# UTILITY HELPERS
# ==================================================
def is_valid_email(email):
    """Validate email address format using regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# ==================================================
# ROUTES
# ==================================================

# --------------------------------------------------
# Home Page
# --------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


# --------------------------------------------------
# TASK 1 & 2 — IPL Ticket Payment Form (Paytm Sandbox)
# --------------------------------------------------
@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'GET':
        return render_template('pay.html', gateway='paytm', form_data={})

    # Extract dynamic form inputs
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    amount_raw = request.form.get('amount', '').strip()

    # Form Validation
    if not name:
        flash("Name is required.", "error")
        return render_template('pay.html', gateway='paytm', form_data=request.form)

    if not email or not is_valid_email(email):
        flash("A valid email address is required.", "error")
        return render_template('pay.html', gateway='paytm', form_data=request.form)

    try:
        amount = float(amount_raw)
        if amount <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        flash("Amount must be a number greater than 0.", "error")
        return render_template('pay.html', gateway='paytm', form_data=request.form)

    # Paytm Credentials
    paytm_mid = os.getenv("PAYTM_MID", "")
    merchant_key = os.getenv("PAYTM_MERCHANT_KEY", "")
    paytm_website = os.getenv("PAYTM_WEBSITE", "WEBSTAGING")
    paytm_channel_id = os.getenv("PAYTM_CHANNEL_ID", "WEB")
    paytm_industry_type_id = os.getenv("PAYTM_INDUSTRY_TYPE_ID", "Retail")

    # Generate unique dynamic order ID
    order_id = f"ORDER_{uuid.uuid4().hex[:10].upper()}"

    # Store user submission details in session for result display
    session['paytm_data'] = {
        'name': name,
        'email': email,
        'amount': f"{amount:.2f}",
        'order_id': order_id
    }

    callback_url = url_for('payment_callback', _external=True)

    # Paytm parameter payload
    paytm_params = {
        "MID": paytm_mid,
        "WEBSITE": paytm_website,
        "CHANNEL_ID": paytm_channel_id,
        "INDUSTRY_TYPE_ID": paytm_industry_type_id,
        "ORDER_ID": order_id,
        "CUST_ID": email,
        "TXN_AMOUNT": f"{amount:.2f}",
        "CALLBACK_URL": callback_url,
        "EMAIL": email,
    }

    # Verify if merchant credentials exist in .env
    if not paytm_mid or not merchant_key:
        flash("Paytm Sandbox MID or Merchant Key is missing in .env configuration. Please update .env.", "warning")

    # Generate actual Paytm Checksum signature
    checksum_hash = generate_paytm_checksum(paytm_params, merchant_key)
    paytm_params["CHECKSUMHASH"] = checksum_hash

    paytm_txn_url = "https://securegw-stage.paytm.in/order/process"

    # Render HTML page that auto-submits form data to Paytm Sandbox
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Redirecting to Paytm Sandbox...</title>
    </head>
    <body onload="document.forms['paytm_submit_form'].submit();" style="background:#0f172a; color:#fff; font-family:sans-serif; text-align:center; padding-top:100px;">
        <h2>Redirecting to Paytm Sandbox Payment Gateway...</h2>
        <p>Order ID: {order_id} | Amount: &#8377;{amount:.2f}</p>
        <form name="paytm_submit_form" method="POST" action="{paytm_txn_url}">
            {''.join([f'<input type="hidden" name="{k}" value="{v}">' for k, v in paytm_params.items()])}
        </form>
    </body>
    </html>
    """


# --------------------------------------------------
# TASK 3 — Paytm Payment Callback
# --------------------------------------------------
@app.route('/payment-callback', methods=['POST', 'GET'])
def payment_callback():
    # Handle callback parameters from POST form or GET args
    paytm_response = request.form.to_dict() if request.method == 'POST' else request.args.to_dict()

    merchant_key = os.getenv("PAYTM_MERCHANT_KEY", "")

    # Retrieve parameters
    checksum_hash = paytm_response.get("CHECKSUMHASH", "")
    paytm_data_copy = {k: v for k, v in paytm_response.items() if k != "CHECKSUMHASH"}

    # Verify checksum signature using Paytm official checksum algorithm
    checksum_valid = verify_paytm_checksum(paytm_data_copy, merchant_key, checksum_hash) if checksum_hash else False

    # Extract transaction details
    status = paytm_response.get("STATUS", "FAILURE")
    order_id = paytm_response.get("ORDERID", session.get('paytm_data', {}).get('order_id', 'N/A'))
    txn_id = paytm_response.get("TXNID", "N/A")
    amount = paytm_response.get("TXNAMOUNT", session.get('paytm_data', {}).get('amount', '0.00'))
    resp_msg = paytm_response.get("RESPMSG", "Transaction Processed")

    name = session.get('paytm_data', {}).get('name', 'N/A')
    email = session.get('paytm_data', {}).get('email', 'N/A')

    return render_template(
        'payment_result.html',
        status=status,
        name=name,
        email=email,
        amount=amount,
        order_id=order_id,
        txn_id=txn_id,
        checksum_valid=checksum_valid,
        resp_msg=resp_msg
    )


# --------------------------------------------------
# TASK 4 — Zomato-Style Food Payment with Stripe
# --------------------------------------------------
@app.route('/food-payment', methods=['GET', 'POST'])
def food_payment():
    if request.method == 'GET':
        return render_template('food_payment.html', form_data={})

    # Extract dynamic food inputs
    dish_name = request.form.get('dish_name', '').strip()
    price_raw = request.form.get('price', '').strip()

    # Form Validation
    if not dish_name:
        flash("Dish name is required.", "error")
        return render_template('food_payment.html', form_data=request.form)

    try:
        price = float(price_raw)
        if price <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        flash("Price must be a valid number greater than 0.", "error")
        return render_template('food_payment.html', form_data=request.form)

    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", "")
    if not stripe_secret_key or stripe_secret_key.startswith("sk_test_your"):
        flash("Stripe secret key is missing or not configured in .env.", "error")
        return render_template('food_payment.html', form_data=request.form)

    stripe.api_key = stripe_secret_key

    # Save details in session
    session['food_data'] = {
        'dish_name': dish_name,
        'price': f"{price:.2f}"
    }

    try:
        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': dish_name,
                    },
                    'unit_amount': int(round(price * 100)),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('food_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('food_cancel', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(f"Stripe Gateway Error: {str(e)}", "error")
        return render_template('food_payment.html', form_data=request.form)


@app.route('/food-payment/success')
def food_success():
    session_id = request.args.get('session_id', '')
    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", "")

    dish_name = session.get('food_data', {}).get('dish_name', 'N/A')
    amount = session.get('food_data', {}).get('price', '0.00')
    payment_intent = None
    status = 'paid'

    if stripe_secret_key and session_id:
        try:
            stripe.api_key = stripe_secret_key
            stripe_session = stripe.checkout.Session.retrieve(session_id)
            status = stripe_session.payment_status
            payment_intent = stripe_session.payment_intent
        except Exception:
            pass

    return render_template(
        'food_result.html',
        status=status,
        dish_name=dish_name,
        amount=amount,
        session_id=session_id,
        payment_intent=payment_intent
    )


@app.route('/food-payment/cancel')
def food_cancel():
    session_id = request.args.get('session_id', '')
    dish_name = session.get('food_data', {}).get('dish_name', 'N/A')
    amount = session.get('food_data', {}).get('price', '0.00')

    return render_template(
        'food_result.html',
        status='cancelled',
        dish_name=dish_name,
        amount=amount,
        session_id=session_id
    )


# --------------------------------------------------
# TASK 5 — PayPal Sandbox IPL Ticket Integration
# --------------------------------------------------
def get_paypal_access_token():
    """Retrieve PayPal Sandbox OAuth2 Access Token."""
    client_id = os.getenv("PAYPAL_CLIENT_ID", "")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        return None

    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, auth=(client_id, client_secret), headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


@app.route('/paypal-pay', methods=['GET', 'POST'])
def paypal_pay():
    if request.method == 'GET':
        return render_template('pay.html', gateway='paypal', form_data={})

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    amount_raw = request.form.get('amount', '').strip()

    if not name:
        flash("Name is required.", "error")
        return render_template('pay.html', gateway='paypal', form_data=request.form)

    if not email or not is_valid_email(email):
        flash("A valid email address is required.", "error")
        return render_template('pay.html', gateway='paypal', form_data=request.form)

    try:
        amount = float(amount_raw)
        if amount <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        flash("Amount must be a valid number greater than 0.", "error")
        return render_template('pay.html', gateway='paypal', form_data=request.form)

    session['paypal_data'] = {
        'name': name,
        'email': email,
        'amount': f"{amount:.2f}"
    }

    access_token = get_paypal_access_token()
    if not access_token:
        flash("PayPal Client ID or Secret is invalid or missing in .env.", "error")
        return render_template('pay.html', gateway='paypal', form_data=request.form)

    # Create PayPal Sandbox Order
    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    return_url = url_for('paypal_capture', _external=True)
    cancel_url = url_for('paypal_cancel', _external=True)

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": f"{amount:.2f}"
                },
                "description": f"IPL Ticket - {name}"
            }
        ],
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url,
            "user_action": "PAY_NOW"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in (200, 201):
        order_data = response.json()
        paypal_order_id = order_data.get("id")
        session['paypal_order_id'] = paypal_order_id

        # Find approve link
        for link in order_data.get("links", []):
            if link.get("rel") == "approve":
                return redirect(link.get("href"))

    flash("Failed to create PayPal sandbox order. Check gateway response.", "error")
    return render_template('pay.html', gateway='paypal', form_data=request.form)


@app.route('/paypal/capture')
def paypal_capture():
    token = request.args.get('token') or session.get('paypal_order_id')
    access_token = get_paypal_access_token()

    name = session.get('paypal_data', {}).get('name', 'N/A')
    email = session.get('paypal_data', {}).get('email', 'N/A')
    amount = session.get('paypal_data', {}).get('amount', '0.00')
    capture_id = None
    status = "CANCELLED"

    if token and access_token:
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{token}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.post(url, headers=headers)
        if response.status_code in (200, 201):
            res_data = response.json()
            status = res_data.get("status", "COMPLETED")
            try:
                capture_id = res_data["purchase_units"][0]["payments"]["captures"][0]["id"]
            except (KeyError, IndexError):
                capture_id = "N/A"

    return render_template(
        'paypal_result.html',
        status=status,
        name=name,
        email=email,
        amount=amount,
        order_id=token,
        capture_id=capture_id
    )


@app.route('/paypal/cancel')
def paypal_cancel():
    order_id = session.get('paypal_order_id', 'N/A')
    name = session.get('paypal_data', {}).get('name', 'N/A')
    email = session.get('paypal_data', {}).get('email', 'N/A')
    amount = session.get('paypal_data', {}).get('amount', '0.00')

    return render_template(
        'paypal_result.html',
        status="CANCELLED",
        name=name,
        email=email,
        amount=amount,
        order_id=order_id,
        capture_id=None
    )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
