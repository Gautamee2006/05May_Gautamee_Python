import os
import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import stripe
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def send_email_view(request):
    """
    POST /api/send-email/
    Accepts: { "email": "user@example.com" }
    Uses Mailgun API via requests package and environment variables.
    Returns: JSON indicating success or failure.
    """
    if request.method == 'GET':
        return Response({
            'info': 'Send a POST request to this endpoint with JSON body: {"email": "user@example.com"}'
        }, status=status.HTTP_200_OK)

    email = request.data.get('email')
    if not email:
        return Response(
            {'success': False, 'message': 'Email address is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    api_key = getattr(settings, 'MAILGUN_API_KEY', os.getenv('MAILGUN_API_KEY', ''))
    domain = getattr(settings, 'MAILGUN_DOMAIN', os.getenv('MAILGUN_DOMAIN', ''))
    sender = getattr(settings, 'MAILGUN_SENDER_EMAIL', os.getenv('MAILGUN_SENDER_EMAIL', ''))

    if not api_key or not domain:
        return Response(
            {'success': False, 'message': 'Mailgun credentials are not configured.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    mailgun_url = f"https://api.mailgun.net/v3/{domain}/messages"

    try:
        response = requests.post(
            mailgun_url,
            auth=("api", api_key),
            data={
                "from": sender or f"Mailgun Sandbox <postmaster@{domain}>",
                "to": [email],
                "subject": "Welcome to Our Platform!",
                "text": "Thank you for joining our platform. We are happy to have you!"
            },
            timeout=10
        )

        if response.status_code == 200:
            return Response(
                {'success': True, 'message': 'Welcome email sent successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': False, 'message': f'Mailgun API error: {response.text}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'success': False, 'message': f'Failed to send email: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def send_sms_view(request):
    """
    POST /api/send-sms/
    Accepts: { "phone_number": "+1234567890", "message": "Hello!" }
    Uses Twilio Python SDK and environment variables.
    Returns: JSON indicating success or failure.
    """
    if request.method == 'GET':
        return Response({
            'info': 'Send a POST request to this endpoint with JSON body: {"phone_number": "+1234567890", "message": "Your message"}'
        }, status=status.HTTP_200_OK)

    phone_number = request.data.get('phone_number')
    message_text = request.data.get('message')

    if not phone_number or not message_text:
        return Response(
            {'success': False, 'message': 'Both phone_number and message are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', os.getenv('TWILIO_ACCOUNT_SID', ''))
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', os.getenv('TWILIO_AUTH_TOKEN', ''))
    from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', os.getenv('TWILIO_PHONE_NUMBER', ''))

    if not account_sid or not auth_token or not from_number:
        return Response(
            {'success': False, 'message': 'Twilio credentials are not configured.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        client = Client(account_sid, auth_token)
        sms = client.messages.create(
            body=message_text,
            from_=from_number,
            to=phone_number
        )
        return Response(
            {'success': True, 'message': 'SMS sent successfully.', 'sid': sms.sid},
            status=status.HTTP_200_OK
        )
    except TwilioRestException as e:
        return Response(
            {'success': False, 'message': f'Twilio API error: {e.msg}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'success': False, 'message': f'Failed to send SMS: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def pay_view(request):
    """
    POST /api/pay/
    Accepts: { "amount": 1000, "currency": "usd" }
    Uses Stripe test API functionality and environment variables.
    Returns: JSON with payment status and transaction ID.
    """
    if request.method == 'GET':
        return Response({
            'info': 'Send a POST request to this endpoint with JSON body: {"amount": 1000, "currency": "usd"}'
        }, status=status.HTTP_200_OK)

    amount = request.data.get('amount')
    currency = request.data.get('currency', 'usd')

    if amount is None:
        return Response(
            {'payment_status': 'failed', 'message': 'Amount is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        amount_int = int(amount)
        if amount_int <= 0:
            return Response(
                {'payment_status': 'failed', 'message': 'Amount must be greater than zero.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (ValueError, TypeError):
        return Response(
            {'payment_status': 'failed', 'message': 'Invalid amount format.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    stripe_key = getattr(settings, 'STRIPE_SECRET_KEY', os.getenv('STRIPE_SECRET_KEY', ''))

    if not stripe_key:
        return Response(
            {'payment_status': 'failed', 'message': 'Stripe secret key is not configured.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    stripe.api_key = stripe_key

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_int,
            currency=str(currency).lower(),
            payment_method_types=['card'],
            description='Test payment simulation'
        )
        return Response(
            {
                'payment_status': payment_intent.get('status', 'succeeded'),
                'transaction_id': payment_intent.get('id')
            },
            status=status.HTTP_200_OK
        )
    except stripe.error.StripeError as e:
        return Response(
            {
                'payment_status': 'failed',
                'message': f'Stripe API error: {str(e.user_message if hasattr(e, "user_message") else e)}'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                'payment_status': 'failed',
                'message': f'Payment processing error: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def google_login_view(request):
    """
    POST /api/google-login/
    Accepts: { "id_token": "..." } or { "access_token": "..." }
    Verifies Google user token, creates or gets Django user, and returns JWT tokens.
    """
    if request.method == 'GET':
        return Response({
            'info': 'Send a POST request to this endpoint with JSON body: {"id_token": "your_google_id_token"}'
        }, status=status.HTTP_200_OK)

    id_token_str = request.data.get('id_token')
    access_token_str = request.data.get('access_token')

    if not id_token_str and not access_token_str:
        return Response(
            {'success': False, 'message': 'id_token or access_token is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_email = None
    first_name = ''
    last_name = ''

    try:
        if id_token_str:
            resp = requests.get(
                'https://oauth2.googleapis.com/tokeninfo',
                params={'id_token': id_token_str},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                user_email = data.get('email')
                first_name = data.get('given_name', '')
                last_name = data.get('family_name', '')
            else:
                return Response(
                    {'success': False, 'message': 'Invalid Google ID token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif access_token_str:
            resp = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token_str}'},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                user_email = data.get('email')
                first_name = data.get('given_name', '')
                last_name = data.get('family_name', '')
            else:
                return Response(
                    {'success': False, 'message': 'Invalid Google access token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
    except Exception as e:
        return Response(
            {'success': False, 'message': f'Failed to authenticate with Google: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if not user_email:
        return Response(
            {'success': False, 'message': 'Could not retrieve email from Google token.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user, created = User.objects.get_or_create(
        username=user_email,
        defaults={
            'email': user_email,
            'first_name': first_name,
            'last_name': last_name
        }
    )

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            'success': True,
            'message': 'Google authentication successful.',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        },
        status=status.HTTP_200_OK
    )
