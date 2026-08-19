from django.test import TestCase, Client
from django.urls import reverse
from profiles.models import Profile
from profiles.forms import ProfileForm

class ProfileAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_01_dashboard_empty(self):
        """TEST 1: Open /profiles/ dashboard when empty"""
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Social Profile Manager")
        self.assertContains(response, "No profiles found.")

    def test_02_create_profile_success(self):
        """TEST 2 & 3: Create profile with valid data and verify persistence on dashboard"""
        data = {
            'username': 'abc',
            'email': 'abc@gmail.com',
            'age': 20,
            'bio': 'Python Django Developer',
            'is_public': True
        }
        response = self.client.post(reverse('profile_create'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirects to profile list
        self.assertEqual(Profile.objects.count(), 1)
        profile = Profile.objects.first()
        self.assertEqual(profile.username, 'abc')
        self.assertEqual(profile.email, 'abc@gmail.com')
        self.assertEqual(profile.age, 20)
        self.assertEqual(profile.bio, 'Python Django Developer')
        self.assertTrue(profile.is_public)

        # TEST 3: Confirm profile appears on dashboard
        response_dash = self.client.get(reverse('profile_list'))
        self.assertContains(response_dash, 'abc')
        self.assertContains(response_dash, 'abc@gmail.com')
        self.assertContains(response_dash, 'Public')

    def test_04_edit_profile(self):
        """TEST 4: Edit profile information and confirm update"""
        profile = Profile.objects.create(
            username='original_user',
            email='user@gmail.com',
            age=25,
            bio='Old bio',
            is_public=False
        )

        update_data = {
            'username': 'updated_user',
            'email': 'updated@gmail.com',
            'age': 26,
            'bio': 'Updated bio description',
            'is_public': True
        }
        response = self.client.post(reverse('profile_edit', kwargs={'id': profile.id}), data=update_data)
        self.assertEqual(response.status_code, 302)
        
        profile.refresh_from_db()
        self.assertEqual(profile.username, 'updated_user')
        self.assertEqual(profile.age, 26)
        self.assertTrue(profile.is_public)

    def test_05_export_csv(self):
        """TEST 5: Export CSV functionality and context manager usage"""
        Profile.objects.create(
            username='exporter',
            email='export@gmail.com',
            age=30,
            bio='Bio text',
            is_public=True
        )
        response = self.client.get(reverse('profile_export'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('attachment; filename="profiles.csv"' in response['Content-Disposition'])

        csv_text = response.content.decode('utf-8')
        self.assertIn('ID,Username,Email,Age,Bio,Is Public', csv_text)
        self.assertIn('exporter', csv_text)
        self.assertIn('export@gmail.com', csv_text)

    def test_06_invalid_age_validation(self):
        """TEST 6: Validation error for age <= 13 (e.g. 10 or 13)"""
        form1 = ProfileForm(data={'username': 'kid1', 'email': 'kid1@gmail.com', 'age': 10, 'bio': '', 'is_public': True})
        self.assertFalse(form1.is_valid())
        self.assertIn('Age should be greater than 13.', form1.errors['age'])

        form2 = ProfileForm(data={'username': 'kid2', 'email': 'kid2@gmail.com', 'age': 13, 'bio': '', 'is_public': True})
        self.assertFalse(form2.is_valid())
        self.assertIn('Age should be greater than 13.', form2.errors['age'])

        # Form submission test via client
        response = self.client.post(reverse('profile_create'), data={'username': 'kid', 'email': 'kid@gmail.com', 'age': 12, 'is_public': True})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Age should be greater than 13.')

    def test_07_invalid_email_validation(self):
        """TEST 7: Validation error for invalid email format"""
        form = ProfileForm(data={'username': 'invalid_email_user', 'email': 'not-an-email', 'age': 20, 'is_public': True})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

        response = self.client.post(reverse('profile_create'), data={'username': 'bad_mail', 'email': 'invalid_email', 'age': 20, 'is_public': True})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')
