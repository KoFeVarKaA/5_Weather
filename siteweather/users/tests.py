import time

from django.urls import reverse
from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY

# Create your tests here.

class TestRegistrationAuthorization(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("users:registration")
        self.registration_data = {
            "username": "testUser",
            "password1": "testPassword9991", 
            "password2": "testPassword9991",
        }
        self.authorization_data  = {
            "username": "testUser2",
            "password": "testPassword9992",  
        }
    
        User.objects.create_user(**self.authorization_data)
        self.user_count = 1

    def test_registration_success(self):
        self.client.post(self.register_url, self.registration_data)

        self.assertEqual(User.objects.count(), self.user_count + 1)

    def test_registration_nonunique_login(self):
        data = {
            "username": "testUser3",
            "password": "testPassword9993"
        }
        User.objects.create_user(**data)
        response = self.client.post(self.register_url, data)

        self.assertContains(response, "Пользователь с таким именем уже существует.")

    def test_authorezation_success(self):
        login_success = self.client.login(**self.authorization_data)

        self.assertTrue(login_success)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_session_expiration(self):
        settings.SESSION_COOKIE_AGE = 1
        response = self.client.login(**self.authorization_data )
        time.sleep(2)

        self.assertNotIn(SESSION_KEY, self.client.session)
        response = self.client.get(reverse("home"))
        self.assertFalse(response.context['user'].is_authenticated)