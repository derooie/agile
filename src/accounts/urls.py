from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    path('registration/', views.RegistrationView.as_view(template_name='accounts/registration.html'),
         name='registration'),
    path('settings/<int:pk>', views.SettingsView.as_view(), name='settings'),
]
