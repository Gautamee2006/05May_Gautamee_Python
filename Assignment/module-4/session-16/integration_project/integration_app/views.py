import logging
import secrets
import string
import requests
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

from integration_app.models import OTPVerification
from integration_app.forms import RegistrationForm, PhoneOTPForm, OTPVerifyForm

logger = logging.getLogger(__name__)


def home(request):
    """Homepage showing dynamic user greeting, OAuth status, and OTP status."""
    user_otp_record = None
    if request.user.is_authenticated:
        user_otp_record = OTPVerification.objects.filter(
            user=request.user,
            is_verified=True
        ).order_by('-created_at').first()

    context = {
        'user_otp_record': user_otp_record
    }
    return render(request, 'integration_app/home.html', context)


def register_view(request):
    """User registration view with Mailgun welcome email integration."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Trigger Mailgun Welcome Email
            send_welcome_email(user)

            messages.success(request, f"Account created for {user.username}! You can now log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = RegistrationForm()

    return render(request, 'integration_app/register.html', {'form': form})


def send_welcome_email(user):
    """Send welcome email to newly registered user via Mailgun API using requests."""
    api_key = getattr(settings, 'MAILGUN_API_KEY', '')
    domain = getattr(settings, 'MAILGUN_DOMAIN', '')
    from_email = getattr(settings, 'MAILGUN_FROM_EMAIL', '') or f"Welcome <postmaster@{domain}>"

    if not api_key or not domain or api_key == 'your_mailgun_api_key_here':
        logger.warning(f"Mailgun credentials not configured. Skipping welcome email for {user.username}.")
        return

    url = f"https://api.mailgun.net/v3/{domain}/messages"
    subject = "Welcome to Integration App!"
    body = (
        f"Hello {user.username},\n\n"
        "Welcome to Integration App!\n\n"
        "Your account has been created successfully.\n\n"
        "Thank you for joining us."
    )

    try:
        response = requests.post(
            url,
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": [user.email],
                "subject": subject,
                "text": body
            },
            timeout=10
        )
        if response.status_code == 200:
            logger.info(f"Mailgun welcome email sent successfully to {user.email}")
        else:
            logger.error(f"Mailgun API returned error status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send welcome email via Mailgun: {str(e)}")


def login_view(request):
    """User login view supporting standard authentication and Google OAuth link."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'integration_app/login.html', {'form': form})


def logout_view(request):
    """Log out the current user and redirect to homepage."""
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def send_otp_view(request):
    """Generate 6-digit SMS OTP, store in database, and dispatch via Twilio API."""
    if request.method == 'POST':
        form = PhoneOTPForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            # Check cooldown (30 seconds)
            last_otp = OTPVerification.objects.filter(
                user=request.user,
                phone_number=phone_number
            ).order_by('-created_at').first()

            if last_otp and (timezone.now() - last_otp.created_at).total_seconds() < 30:
                messages.error(request, "Please wait 30 seconds before requesting a new OTP.")
                return redirect('verify-otp')

            # Invalidate any old unverified OTPs for this phone number / user
            OTPVerification.objects.filter(
                user=request.user,
                phone_number=phone_number,
                is_verified=False
            ).update(expires_at=timezone.now())

            # Generate secure random 6-digit OTP
            otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
            expires_at = timezone.now() + timedelta(minutes=5)

            # Save model record
            otp_record = OTPVerification.objects.create(
                user=request.user,
                phone_number=phone_number,
                otp=otp_code,
                expires_at=expires_at
            )

            # Save in session for verification workflow
            request.session['otp_phone_number'] = phone_number
            request.session['otp_record_id'] = otp_record.id

            # Dispatch SMS via Twilio API
            send_sms_otp(phone_number, otp_code, request)

            messages.success(request, f"OTP sent successfully to {phone_number}.")
            return redirect('verify-otp')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        # Pre-fill phone if available in session
        initial_phone = request.session.get('otp_phone_number', '')
        form = PhoneOTPForm(initial={'phone_number': initial_phone})

    return render(request, 'integration_app/otp.html', {'form': form, 'step': 'send'})


def send_sms_otp(phone_number, otp_code, request):
    """Send SMS OTP via Twilio SDK safely handling API keys."""
    sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    twilio_number = getattr(settings, 'TWILIO_PHONE_NUMBER', '')

    if not sid or not token or sid == 'your_twilio_account_sid_here':
        logger.warning("Twilio API credentials missing or default. Simulated OTP log.")
        messages.info(request, f"Development Mode: Your generated OTP is {otp_code} (Valid for 5 minutes).")
        return

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        message = client.messages.create(
            body=f"Your Integration App OTP is {otp_code}. It is valid for 5 minutes.",
            from_=twilio_number,
            to=phone_number
        )
        logger.info(f"Twilio SMS dispatched with SID: {message.sid}")
    except Exception as e:
        logger.error(f"Twilio SMS sending failed: {str(e)}")
        messages.error(request, "Failed to deliver SMS via Twilio API. (Development OTP is available in dev mode).")
        messages.info(request, f"Development Mode: Your generated OTP is {otp_code}.")


@login_required
def verify_otp_view(request):
    """Verify 6-digit OTP code against latest database record."""
    phone_number = request.session.get('otp_phone_number')
    otp_record_id = request.session.get('otp_record_id')

    # Fetch latest OTP record
    otp_record = None
    if otp_record_id:
        otp_record = OTPVerification.objects.filter(id=otp_record_id, user=request.user).first()
    if not otp_record and phone_number:
        otp_record = OTPVerification.objects.filter(user=request.user, phone_number=phone_number).order_by('-created_at').first()

    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']

            if not otp_record:
                messages.error(request, "No active OTP request found. Please request a new OTP.")
                return redirect('send-otp')

            if otp_record.is_verified:
                messages.info(request, "This OTP has already been verified successfully.")
                return redirect('profile')

            if otp_record.attempts >= 5:
                messages.error(request, "Maximum verification attempts (5) exceeded. Please request a new OTP.")
                return redirect('send-otp')

            if otp_record.is_expired():
                messages.error(request, "OTP expired. Please request a new OTP.")
                return redirect('send-otp')

            if entered_otp == otp_record.otp:
                otp_record.is_verified = True
                otp_record.save()
                messages.success(request, "OTP verified successfully!")
                return render(request, 'integration_app/success.html', {'message': 'Your phone number has been verified successfully!'})
            else:
                otp_record.attempts += 1
                otp_record.save()
                remaining = max(0, 5 - otp_record.attempts)
                if remaining > 0:
                    messages.error(request, f"Invalid OTP. You have {remaining} attempts remaining.")
                else:
                    messages.error(request, "Invalid OTP. Maximum attempts exceeded. Please request a new OTP.")
                    return redirect('send-otp')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = OTPVerifyForm()

    context = {
        'form': form,
        'step': 'verify',
        'phone_number': phone_number or (otp_record.phone_number if otp_record else '')
    }
    return render(request, 'integration_app/otp.html', context)


@login_required
def resend_otp_view(request):
    """Resend a new 6-digit OTP with cooldown enforcement."""
    phone_number = request.session.get('otp_phone_number')

    if not phone_number:
        # Check if user has previous record
        last_record = OTPVerification.objects.filter(user=request.user).order_by('-created_at').first()
        if last_record:
            phone_number = last_record.phone_number

    if not phone_number:
        messages.error(request, "Please enter your phone number to request an OTP.")
        return redirect('send-otp')

    # Check cooldown (30 seconds)
    last_otp = OTPVerification.objects.filter(
        user=request.user,
        phone_number=phone_number
    ).order_by('-created_at').first()

    if last_otp and (timezone.now() - last_otp.created_at).total_seconds() < 30:
        messages.error(request, "Please wait 30 seconds before resending OTP.")
        return redirect('verify-otp')

    # Invalidate previous unverified OTPs
    OTPVerification.objects.filter(
        user=request.user,
        phone_number=phone_number,
        is_verified=False
    ).update(expires_at=timezone.now())

    # Generate new random 6-digit OTP
    new_otp = ''.join(secrets.choice(string.digits) for _ in range(6))
    expires_at = timezone.now() + timedelta(minutes=5)

    otp_record = OTPVerification.objects.create(
        user=request.user,
        phone_number=phone_number,
        otp=new_otp,
        expires_at=expires_at
    )

    request.session['otp_phone_number'] = phone_number
    request.session['otp_record_id'] = otp_record.id

    # Resend SMS via Twilio
    send_sms_otp(phone_number, new_otp, request)

    messages.success(request, f"A new OTP has been sent to {phone_number}.")
    return redirect('verify-otp')


@login_required
def profile_view(request):
    """User profile view displaying username, email, names, and OTP verification status."""
    latest_verification = OTPVerification.objects.filter(
        user=request.user,
        is_verified=True
    ).order_by('-created_at').first()

    context = {
        'user': request.user,
        'verification': latest_verification
    }
    return render(request, 'integration_app/profile.html', context)
