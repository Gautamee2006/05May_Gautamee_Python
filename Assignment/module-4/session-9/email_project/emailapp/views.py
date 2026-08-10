from django.http import HttpResponse
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

def test_email(request):

    send_mail(
        'Django Test Email',
        'Hello! This is a test email sent using Django SMTP.',
        'yourgmail@gmail.com',
        ['yourtestemail@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Test email sent successfully!')


def send_password_reset_email(request, user_email):

    reset_link = 'http://127.0.0.1:8000/reset-password/'

    subject = 'Reset Your Password'

    message = f"""
Hello,

We received a request to reset your password.

Click the link below to reset your password:

{reset_link}

If you did not request a password reset, you can safely ignore this email.

Thanks,
Your App Team
"""

    send_mail(
        subject,
        message,
        'gautamikakadiya11@gmail.com',
        [user_email],
        fail_silently=False,
    )

    return HttpResponse('Password reset email sent successfully!')

def send_order_confirmation(request):

    context = {
        'user_name': 'Gautamee',
        'order_id': 'ORD1001',
        'restaurant': 'Food Corner',
        'items': 'Pizza, Burger, Cold Drink',
        'total': 499,
    }

    html_content = render_to_string(
        'emails/order_confirmation.html',
        context
    )

    subject = 'Your Order Has Been Confirmed! 🍔'

    text_content = 'Your food order has been successfully placed.'

    email = EmailMultiAlternatives(
        subject,
        text_content,
        'gautamikakadiya11@gmail.com',
        ['granthkakadiya11@gmail.com'],
    )

    email.attach_alternative(
        html_content,
        'text/html'
    )

    email.send()

    return HttpResponse(
        'Order confirmation email sent successfully!'
    )

def send_ipl_welcome_email(request):

    subject = '🏏 Welcome to IPL Fantasy League – Build Your Dream Team!'

    text_content = """
Welcome to IPL Fantasy League!

Build your dream team, select your favorite players,
earn fantasy points and compete with your friends.

Let the fantasy begin!
"""

    html_content = """
<!DOCTYPE html>

<html>

<head>

    <meta charset="UTF-8">

    <title>IPL Fantasy League</title>

</head>

<body style="
    margin:0;
    padding:0;
    background:#f4f4f4;
    font-family:Arial,sans-serif;
">

    <div style="
        width:600px;
        margin:40px auto;
        background:white;
        padding:40px;
        text-align:center;
    ">

        <h1 style="
            color:#ff6b00;
            font-size:32px;
        ">
            🏏 Welcome to IPL Fantasy League!
        </h1>

        <p style="font-size:18px;">
            Build Your Dream Team!
        </p>

        <p style="
            color:#555;
            line-height:1.6;
        ">
            Get ready to create your ultimate cricket team
            and compete with your friends.
        </p>

        <div style="
            background:#f8f8f8;
            padding:20px;
            margin:25px 0;
        ">

            <h2>
                🔥 Pick Your Players
            </h2>

            <p>
                Choose your favorite players,
                earn fantasy points and climb the leaderboard.
            </p>

        </div>

        <h2>
            🏆 Let the Fantasy Begin!
        </h2>

        <p style="color:#777;">
            Good luck and have fun!
        </p>

    </div>

</body>

</html>
"""

    email = EmailMultiAlternatives(
        subject,
        text_content,
        'gautamikakadiya11@gmail.com',
        ['granthkakadiya11@gmail.com'],
    )

    email.attach_alternative(
        html_content,
        'text/html'
    )

    email.send()

    return HttpResponse(
        'IPL Fantasy welcome email sent successfully!'
    )