from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'testPassword')

    def test_no_access(self):
        self.client.login(username='test_user', password='wrongTestPassword')
        response = self.client.get(reverse('accounts:registration'))
        self.assertEqual(response.status_code, 302)

    def test_user_authenticated(self):
        self.client.login(username='test_user', password='testPassword')
        response = self.client.get(reverse('accounts:registration'))
        self.assertEqual(response.status_code, 200)
