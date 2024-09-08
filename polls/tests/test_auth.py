from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTest(TestCase):
    """Test for checking the authentication"""

    def setUp(self):
        """Create a user for testing purposes."""
        self.user = User.objects.create_user(username='test', password='1234')

    def test_success_login(self):
        """
        If the user enters the correct username and password,
        they should be logged in and redirected to the Index page with a greeting context.
        """
        login_successful = self.client.login(username='test', password='1234')
        self.assertTrue(login_successful)

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, test')

    def test_failed_login(self):
        """
        If the user enters incorrect username or password,
        they should not be able to log in.
        """
        # Attempt login with incorrect username
        login_failed = self.client.login(username='wrong_username', password='1234')
        self.assertFalse(login_failed)

        # Attempt login with incorrect password
        login_failed = self.client.login(username='test', password='wrong_password')
        self.assertFalse(login_failed)

    def test_success_logout(self):
        """
        If the user is logged in and then logs out,
        they should be redirected to the login page, and login status should be False.
        """
        self.client.login(username='test', password='1234')
        response = self.client.get(reverse('logout'))
        # Ensure the user is logged out
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, 'Welcome back, test')
