from django.urls import path
from .views import send_email_view, send_sms_view, pay_view, google_login_view

urlpatterns = [
    path('send-email/', send_email_view, name='send-email'),
    path('send-sms/', send_sms_view, name='send-sms'),
    path('pay/', pay_view, name='pay'),
    path('google-login/', google_login_view, name='google-login'),
]
