from django import forms

from accounts.models import AgileUser, CHART_CHOICES


class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AgileUser
        exclude = ('team', 'user',)

        widgets = {
            'chart_type': forms.Select(choices=CHART_CHOICES),
        }
