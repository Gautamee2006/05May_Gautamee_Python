import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        label="Password",
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username is required.")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class PhoneOTPForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1234567890 or 9876543210',
            'autocomplete': 'tel'
        }),
        label="Mobile Phone Number"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '').strip()
        if not phone_number:
            raise ValidationError("Phone number is required.")
        # E.164 pattern or generic phone format check
        cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
        if not re.match(r'^\+?[0-9]{7,15}$', cleaned):
            raise ValidationError("Enter a valid phone number (7-15 digits, optional + prefix).")
        return cleaned


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control otp-input',
            'placeholder': '123456',
            'maxlength': '6',
            'pattern': '[0-9]{6}',
            'inputmode': 'numeric',
            'autocomplete': 'one-time-code'
        }),
        label="6-Digit OTP Code"
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp', '').strip()
        if not otp.isdigit() or len(otp) != 6:
            raise ValidationError("OTP must be exactly 6 numeric digits.")
        return otp
