from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class SignInTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='testuser@example.com',
            password='securepassword'
        )
        self.login_url = reverse('login')  
    def test_valid_login(self):
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('projects'))

    
    
    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect status code
        self.assertRedirects(response, reverse('login'))  # Verify redirection to login page
        # Check if an error message is in the session or messages framework
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(message.message == "Invalid Password or Username" for message in messages))
