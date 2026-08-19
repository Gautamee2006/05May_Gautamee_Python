from django.test import TestCase
from django.urls import reverse
from .models import UserProfile
from .forms import UserProfileForm

class UserProfileTests(TestCase):
    def test_create_profile_valid_data(self):
        """Test creating a profile with valid data (age > 13)."""
        response = self.client.post(reverse('create_profile'), {
            'username': 'abc',
            'age': 20,
            'is_public': True
        })
        self.assertRedirects(response, reverse('profiles'))
        self.assertEqual(UserProfile.objects.count(), 1)
        profile = UserProfile.objects.first()
        self.assertEqual(profile.username, 'abc')
        self.assertEqual(profile.age, 20)
        self.assertTrue(profile.is_public)

    def test_create_profile_age_thirteen_error(self):
        """Test age equal to 13 displays validation error 'User must be over 13 years old.'"""
        response = self.client.post(reverse('create_profile'), {
            'username': 'john',
            'age': 13,
            'is_public': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User must be over 13 years old.")
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_create_profile_age_below_thirteen_error(self):
        """Test age below 13 displays validation error."""
        response = self.client.post(reverse('create_profile'), {
            'username': 'kid',
            'age': 10,
            'is_public': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User must be over 13 years old.")
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_public_and_private_profiles_display(self):
        """Test that /profiles/ displays both Public and Private profiles correctly."""
        UserProfile.objects.create(username='public_user', age=25, is_public=True)
        UserProfile.objects.create(username='private_user', age=30, is_public=False)

        response = self.client.get(reverse('profiles'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'public_user')
        self.assertContains(response, 'private_user')
        self.assertContains(response, 'Public')
        self.assertContains(response, 'Private')

    def test_empty_profiles_display(self):
        """Test empty state when no profiles exist."""
        response = self.client.get(reverse('profiles'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No profiles found.")

