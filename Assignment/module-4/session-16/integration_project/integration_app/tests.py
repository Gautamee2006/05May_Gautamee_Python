from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from integration_app.models import OTPVerification
from integration_app.forms import RegistrationForm, PhoneOTPForm, OTPVerifyForm


class OTPVerificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123"
        )

    def test_otp_creation_and_expiry(self):
        expires_at = timezone.now() + timedelta(minutes=5)
        otp_record = OTPVerification.objects.create(
            user=self.user,
            phone_number="+1234567890",
            otp="123456",
            expires_at=expires_at
        )

        self.assertFalse(otp_record.is_expired())
        self.assertTrue(otp_record.is_valid())
        self.assertEqual(otp_record.attempts, 0)
        self.assertFalse(otp_record.is_verified)

    def test_otp_expired_logic(self):
        past_time = timezone.now() - timedelta(minutes=1)
        expired_otp = OTPVerification.objects.create(
            user=self.user,
            phone_number="+1234567890",
            otp="654321",
            expires_at=past_time
        )
        self.assertTrue(expired_otp.is_expired())
        self.assertFalse(expired_otp.is_valid())

    def test_max_attempts_invalidation(self):
        expires_at = timezone.now() + timedelta(minutes=5)
        otp_record = OTPVerification.objects.create(
            user=self.user,
            phone_number="+1234567890",
            otp="112233",
            expires_at=expires_at,
            attempts=5
        )
        self.assertFalse(otp_record.is_valid())


class RegistrationFormTest(TestCase):
    def test_valid_registration_form(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123',
            'confirm_password': 'SecurePassword123'
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_mismatched_passwords(self):
        data = {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'Password123',
            'confirm_password': 'DifferentPassword123'
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="Password123!"
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Integration App")

    def test_send_otp_requires_login(self):
        response = self.client.get(reverse('send-otp'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_send_and_verify_otp_flow(self):
        self.client.force_login(self.user)
        send_response = self.client.post(reverse('send-otp'), {'phone_number': '+15551234567'})
        self.assertEqual(send_response.status_code, 302)

        otp_record = OTPVerification.objects.filter(user=self.user).first()
        self.assertIsNotNone(otp_record)
        self.assertEqual(len(otp_record.otp), 6)

        # Verify correct OTP
        verify_response = self.client.post(reverse('verify-otp'), {'otp': otp_record.otp})
        self.assertEqual(verify_response.status_code, 200)
        
        otp_record.refresh_from_db()
        self.assertTrue(otp_record.is_verified)
