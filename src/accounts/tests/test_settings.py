from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import AgileUser, Team
from accounts.forms import AppSettingsForm


class SettingsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'testPassword')
        self.team = Team.objects.create(team_name='Test team')
        self.agile_user = AgileUser.objects.create(user=self.user, team=self.team)

    def test_settings_view_no_access(self):
        self.client.login(username='test_user', password='wrongTestPassword')
        response = self.client.get(reverse('accounts:settings', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_settings_view_access(self):
        self.client.login(username='test_user', password='testPassword')
        response = self.client.get(reverse('accounts:settings', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    # Valid form data, line is accepted chart type
    def test_form_valid(self):
        form = AppSettingsForm(data={'team': self.team, 'user': self.user, 'chart_type': 'line'})
        self.assertTrue(form.is_valid())

    # Invalid form data
    def test_form_invalid(self):
        form = AppSettingsForm(data={'team': self.team, 'user': self.user, 'chart_type': 'pie'})
        self.assertFalse(form.is_valid())
