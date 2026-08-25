from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime
from functools import wraps
from .models import OTPVerification
from .forms import RegistrationForm, LoginForm, OTPForm, UserProfileForm

def send_otp_to_user_email(user, otp_code):
    """Sends beautifully designed HTML OTP email to user's registered email address."""
    user_name = user.first_name or user.username or "User"
    
    context = {
        'user_name': user_name,
        'otp_code': otp_code,
        'user_email': user.email,
    }
    
    html_content = render_to_string('emails/otp_email.html', context)
    text_content = strip_tags(html_content)
    subject = "Your CineTicket Login Verification Code (OTP)"

    # Console output for dev testing visibility (ASCII safe for Windows cp1252)
    print("\n" + "=" * 60)
    print(f"[EMAIL DESTINATION USER]: {user.email}")
    print(f"[GENERATED OTP CODE]: {otp_code}")
    print("=" * 60 + "\n")

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        print(f"SUCCESS: Beautiful HTML OTP email sent to inbox ({user.email}) via Gmail SMTP!")
    except Exception as e:
        print(f"SMTP WARNING: Could not dispatch HTML email to {user.email} -> {e}")
        print(f"FOR TESTING: Please use the 6-digit OTP code [{otp_code}] printed above!")





def otp_verified_required(view_func):

    """Decorator to ensure user is logged in AND passed OTP verification."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.session.get('otp_verified', False):
            messages.error(request, "Please log in and complete OTP verification to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def register_view(request):
    if request.user.is_authenticated and request.session.get('otp_verified', False):
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in with your email and password.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated and request.session.get('otp_verified', False):
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']

            # Find user by email or username
            user_obj = User.objects.filter(email__iexact=email).first()
            if not user_obj:
                user_obj = User.objects.filter(username__iexact=email).first()

            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    # Successful login credentials, generate OTP
                    otp_obj, created = OTPVerification.objects.get_or_create(
                        user=user,
                        defaults={
                            'otp': '000000',
                            'expires_at': timezone.now() + datetime.timedelta(minutes=3)
                        }
                    )
                    otp_code = otp_obj.generate_new_otp()

                    # Send OTP email to user's registered email address
                    send_otp_to_user_email(user, otp_code)

                    # Store pending user ID in session
                    request.session['pending_otp_user_id'] = user.id
                    messages.info(request, f"Credentials verified! A 6-digit OTP has been sent to your email ({user.email}).")
                    return redirect('verify_otp')

                else:
                    messages.error(request, "Invalid email or password.")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please fill in all fields correctly.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('pending_otp_user_id')
    if not user_id:
        messages.error(request, "Session expired or invalid login attempt. Please log in again.")
        return redirect('login')

    user = get_object_or_404(User, pk=user_id)
    otp_obj = get_object_or_404(OTPVerification, user=user)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp'].strip()

            # 1. Check attempt limit
            if otp_obj.attempts >= 3:
                messages.error(request, "Maximum 3 wrong attempts reached. OTP invalidated. Please request a new OTP.")
                return render(request, 'accounts/otp_verify.html', {'form': form, 'user': user, 'otp_obj': otp_obj})

            # 2. Check expiration
            if otp_obj.is_expired():
                messages.error(request, "OTP expired. Please request a new OTP.")
                return render(request, 'accounts/otp_verify.html', {'form': form, 'user': user, 'otp_obj': otp_obj})

            # 3. Verify OTP
            if entered_otp == otp_obj.otp:
                otp_obj.is_verified = True
                otp_obj.save()

                # Complete authentication
                login(request, user)
                request.session['otp_verified'] = True
                if 'pending_otp_user_id' in request.session:
                    del request.session['pending_otp_user_id']

                messages.success(request, f"Welcome back, {user.first_name or user.username}! Verification successful.")
                return redirect('dashboard')
            else:
                otp_obj.attempts += 1
                otp_obj.save()
                remaining = 3 - otp_obj.attempts
                if remaining > 0:
                    messages.error(request, f"Incorrect OTP. You have {remaining} attempt(s) remaining.")
                else:
                    messages.error(request, "Maximum 3 wrong attempts reached. OTP invalidated. Please request a new OTP.")
        else:
            messages.error(request, "Please enter a valid 6-digit OTP.")
    else:
        form = OTPForm()

    return render(request, 'accounts/otp_verify.html', {
        'form': form,
        'user': user,
        'otp_obj': otp_obj
    })


def resend_otp_view(request):
    user_id = request.session.get('pending_otp_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')

    user = get_object_or_404(User, pk=user_id)
    otp_obj, created = OTPVerification.objects.get_or_create(
        user=user,
        defaults={
            'otp': '000000',
            'expires_at': timezone.now() + datetime.timedelta(minutes=3)
        }
    )
    new_otp = otp_obj.generate_new_otp()

    # Send new OTP email to user's registered email address
    send_otp_to_user_email(user, new_otp)

    messages.success(request, f"A new 6-digit OTP has been sent to your email ({user.email}).")
    return redirect('verify_otp')



@otp_verified_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


@otp_verified_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.username = form.cleaned_data['email'].lower()
            updated_user.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct errors in the profile form.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


def logout_view(request):
    request.session.flush()
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
