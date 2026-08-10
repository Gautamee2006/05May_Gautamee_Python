import random


from django.shortcuts import render, redirect


from django.contrib import messages


from django.core.mail import send_mail


from .forms import ForgotPasswordForm, OTPForm


# ==================================================
# FORGOT PASSWORD
# ==================================================

def forgot_password_view(request):

    if request.method == 'POST':

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            # Get email from form
            email = form.cleaned_data['email']


            # Generate 6 digit OTP
            otp = random.randint(100000, 999999)


            # Store OTP in session
            request.session['otp'] = str(otp)


            # Store email in session
            request.session['reset_email'] = email


            # OTP expires after 5 minutes
            request.session.set_expiry(300)


            # Send OTP email
            send_mail(

                'Password Reset OTP',

                f"""
Hello,

We received a request to reset your password.

Your OTP is:

{otp}

This OTP is valid for 5 minutes.

If you did not request a password reset,
please ignore this email.

Thanks,
Email Project Team
""",

                'yourgmail@gmail.com',

                [email],

                fail_silently=False,
            )


            # Redirect to OTP page
            return redirect('verify_otp')


    else:

        form = ForgotPasswordForm()


    return render(

        request,

        'emails/forgot_password.html',

        {
            'form': form
        }

    )


# ==================================================
# VERIFY OTP
# ==================================================

def verify_otp_view(request):

    # Check OTP session first

    if 'otp' not in request.session:

        messages.error(

            request,

            'OTP expired or not generated. Please request a new OTP.'

        )

        return redirect('forgot_password')


    if request.method == 'POST':

        form = OTPForm(request.POST)


        if form.is_valid():

            # OTP entered by user
            entered_otp = form.cleaned_data['otp']


            # OTP stored in session
            session_otp = request.session.get('otp')


            # Compare OTP
            if session_otp == entered_otp:

                messages.success(

                    request,

                    'OTP verified successfully!'

                )


                # Remove OTP after successful verification
                del request.session['otp']


                return redirect(
                    'password_reset_success'
                )


            else:

                messages.error(

                    request,

                    'Invalid OTP. Please try again.'

                )


    else:

        form = OTPForm()


    return render(

        request,

        'emails/verify_otp.html',

        {
            'form': form
        }

    )


# ==================================================
# PASSWORD RESET SUCCESS
# ==================================================

def password_reset_success(request):

    return render(

        request,

        'emails/password_reset_success.html'

    )