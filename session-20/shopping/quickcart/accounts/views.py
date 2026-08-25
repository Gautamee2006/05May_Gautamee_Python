import random
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import Profile, Address, OTPVerification, RecentlyViewed
from accounts.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, AddressForm, OTPForm

def send_otp_email(user_email, otp_code, purpose="Registration"):
    subject = f"QuickCart - Your OTP for {purpose}"
    plain_message = f"Welcome to QuickCart! Your OTP verification code is {otp_code}. It is valid for 10 minutes."
    
    html_message = f"""
    <div style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; max-width: 550px; margin: 0 auto; padding: 25px; border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;">
        <div style="text-align: center; padding-bottom: 20px; border-bottom: 2px solid #f1f5f9;">
            <h1 style="color: #0f172a; margin: 0; font-size: 26px; font-weight: 800;">Quick<span style="color: #06b6d4;">Cart</span></h1>
            <p style="color: #64748b; margin: 5px 0 0 0; font-size: 14px;">Your Premier E-Commerce Platform</p>
        </div>
        <div style="padding: 25px 10px; text-align: center;">
            <h3 style="color: #1e293b; font-size: 20px; margin-top: 0;">{purpose} Verification Code</h3>
            <p style="color: #475569; font-size: 15px; line-height: 1.5;">Please use the following 6-digit One-Time Password (OTP) to proceed:</p>
            <div style="margin: 25px 0; padding: 18px; background-color: #0f172a; border-radius: 10px; display: inline-block; width: 80%;">
                <span style="font-size: 32px; font-weight: 800; letter-spacing: 8px; color: #38bdf8; font-family: monospace;">{otp_code}</span>
            </div>
            <p style="color: #ef4444; font-size: 13px; font-weight: 600; margin-bottom: 5px;">⚠️ This OTP is valid for 10 minutes only.</p>
            <p style="color: #94a3b8; font-size: 12px;">If you did not request this OTP, please ignore this email.</p>
        </div>
        <div style="text-align: center; padding-top: 15px; border-top: 1px solid #f1f5f9; color: #94a3b8; font-size: 12px;">
            &copy; 2026 QuickCart Inc. All rights reserved.
        </div>
    </div>
    """
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'QuickCart <noreply@quickcart.com>'),
        recipient_list=[user_email],
        html_message=html_message,
        fail_silently=True
    )

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user (inactive until OTP verified)
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Save mobile into profile
            user.profile.mobile = form.cleaned_data.get('mobile')
            user.profile.save()

            # Generate OTP
            otp_code = str(random.randint(100000, 999999))
            OTPVerification.objects.create(user=user, otp_code=otp_code)
            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'registration'

            # Send HTML OTP email
            send_otp_email(user.email, otp_code, purpose="Account Registration")

            messages.success(request, f"Account created! An OTP has been sent to {user.email}.")
            return redirect('accounts:verify_otp')

    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    purpose = request.session.get('otp_purpose', 'registration')

    if not user_id:
        messages.error(request, "No pending OTP verification session found.")
        return redirect('accounts:login')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            input_otp = form.cleaned_data.get('otp')
            otp_record = OTPVerification.objects.filter(user=user, otp_code=input_otp, is_verified=False).last()

            if otp_record:
                otp_record.is_verified = True
                otp_record.save()

                if purpose == 'registration':
                    user.is_active = True
                    user.save()
                    login(request, user)
                    del request.session['otp_user_id']
                    del request.session['otp_purpose']
                    messages.success(request, "Email verified successfully! Welcome to QuickCart.")
                    return redirect('accounts:profile')

                elif purpose == 'reset_password':
                    request.session['reset_user_id'] = user.id
                    del request.session['otp_user_id']
                    del request.session['otp_purpose']
                    messages.success(request, "OTP verified! Please set a new password.")
                    return redirect('accounts:change_password')
            else:
                messages.error(request, "Invalid OTP code. Please try again.")
    else:
        form = OTPForm()

    return render(request, 'accounts/verify_otp.html', {'form': form, 'user_email': user.email, 'purpose': purpose})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        login_input = request.POST.get('username')
        password = request.POST.get('password')

        # Allow login by username or email
        user_obj = User.objects.filter(Q(username=login_input) | Q(email=login_input)).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                    next_url = request.GET.get('next') or 'home'
                    return redirect(next_url)
                else:
                    # Resend OTP if inactive
                    otp_code = str(random.randint(100000, 999999))
                    OTPVerification.objects.create(user=user_obj, otp_code=otp_code)
                    request.session['otp_user_id'] = user_obj.id
                    request.session['otp_purpose'] = 'registration'
                    send_otp_email(user_obj.email, otp_code, purpose="Account Verification")
                    messages.warning(request, "Account is not verified yet. A new OTP has been sent to your email.")
                    return redirect('accounts:verify_otp')
            else:
                messages.error(request, "Invalid password.")
        else:
            messages.error(request, "User account not found.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    profile = request.user.profile
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    recently_viewed = RecentlyViewed.objects.filter(user=request.user)[:8]

    context = {
        'profile': profile,
        'addresses': addresses,
        'recently_viewed': recently_viewed
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user, user=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, user_profile=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=user, user=user)
        p_form = ProfileUpdateForm(instance=profile, user_profile=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            otp_code = str(random.randint(100000, 999999))
            OTPVerification.objects.create(user=user, otp_code=otp_code)
            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'reset_password'

            send_otp_email(user.email, otp_code, purpose="Password Reset")
            messages.success(request, f"Password reset OTP sent to {email}.")
            return redirect('accounts:verify_otp')
        else:
            messages.error(request, "No account found with this email address.")
    return render(request, 'accounts/forgot_password.html')



# --- Address Views ---
@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "New delivery address added successfully!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:profile')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Add New Address'})


@login_required
def edit_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('accounts:profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'title': 'Edit Address'})


@login_required
def delete_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Address removed successfully.")
    return redirect('accounts:profile')


@login_required
def set_default_address_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, f"Default delivery address set to {address.house_flat}, {address.city}.")
    return redirect('accounts:profile')
