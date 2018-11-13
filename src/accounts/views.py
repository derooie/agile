from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView

from accounts.forms import AppSettingsForm
from accounts.models import AgileUser


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class RegistrationView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('accounts:login')
    model = User
    fields = ['username', 'password']

    def form_valid(self, form):
        data = form.cleaned_data
        self.save_user(data)
        return HttpResponseRedirect(reverse('accounts:login'))

    @staticmethod
    def save_user(data):
        User.objects.create(
            username=data.get('username'),
            password=data.get('password')
        )


class SettingsView(LoginRequiredMixin, UpdateView):
    form_class = AppSettingsForm
    template_name = 'accounts/settings.html'
    model = AgileUser

    def get_success_url(self):
        return '/accounts/settings/{}'.format(self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Values updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Settings could not be updated')
        return super().form_valid(form)
