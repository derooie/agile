from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Team, AgileUser
from retrospectives.models import Retrospective, RetrospectiveNumber
from retrospectives.views import IndexView


class RetrospectiveDetailsViewTest(TestCase):
    fixtures = ['auth', 'accounts', 'retrospectives']

    def setUp(self):
        self.client = Client()

    def test_access_to_index(self):
        self.client.login(username='patrick', password='red7net2')
        response = self.client.get(reverse('retrospectives:details', kwargs={'slug': 'sprint-1'}))
        self.assertEqual(response.status_code, 200)

    # def test_exception(self):
    #     self.client.login(username='patrick', password='red7net2')
    #     response = self.client.get(reverse('retrospectives:details', kwargs={'slug': 'sprint-99'}))
    #     x = self.assertRaises(RetrospectiveNumber.DoesNotExist)
    #     # self.assertRaises(RetrospectiveNumber.DoesNotExist, slug='sprint-78')
    #     y = x.msg
    #     self.assertEqual(str(y), 'sprint-4')

    def test_no_access_to_index(self):
        self.client.login(username='patrick', password='wrongTestPassword')
        response = self.client.get(reverse('retrospectives:details', kwargs={'slug': 'sprint-1'}))
        self.assertEqual(response.status_code, 302)

    def test_check_redirect(self):
        response = self.client.get(reverse('retrospectives:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login?next=/retrospectives/', status_code=302, target_status_code=301)

    # def test_index_view_context(self):
    #     self.client.login(username='patrick', password='red7net2')
    #     response = self.client.get(reverse('retrospectives:index'))
    #     print('Response')
    #     print(response.status_code)
    #     pol = response.context[-1]['retrospectives']
    #     for r in pol:
    #         print(r.sprint_name)
