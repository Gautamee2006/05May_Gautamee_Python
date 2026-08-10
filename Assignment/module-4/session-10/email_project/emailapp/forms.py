from django import forms


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email',
                'autocomplete': 'email'
            }
        )
    )


class OTPForm(forms.Form):

    otp = forms.CharField(
        label='OTP',
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter 6-digit OTP',
                'autocomplete': 'one-time-code'
            }
        )
    )