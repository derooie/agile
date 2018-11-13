from django import forms

from retrospectives.models import RetrospectiveNumber, RetrospectiveUserFeedback

TEXT_WIDGET = {'cols': 20, 'rows': 5, 'class': 'form-control'}
SELECT_WIDGET = {'class': 'form-control'}


class AddRetrospectiveValuesForm(forms.ModelForm):
    # def clean(self):
    #     cleaned_data = super().clean()
    #     great = cleaned_data.get("great")
    #     if great is None:
    #         msg = 'Field is empty'
    #         self.add_error('great', msg)
    #
    #     better = cleaned_data.get("better")
    #     if better is None:
    #         msg = 'Field is empty'
    #         self.add_error('better', msg)

    class Meta:
        model = RetrospectiveNumber
        exclude = ('team', 'sprint_number', 'user', 'great', 'better')

        FUN_AND_VALUE_CHOICES = ((1, 'Terrible'), (2, 'Not so good'), (3, 'Good'), (4, 'Great'))


        widgets = {
            'fun': forms.Select(choices=FUN_AND_VALUE_CHOICES, attrs=SELECT_WIDGET),
            'value': forms.Select(choices=FUN_AND_VALUE_CHOICES, attrs=SELECT_WIDGET),
            # 'great': forms.Textarea(attrs=TEXT_WIDGET),
            # 'better': forms.Textarea(attrs=TEXT_WIDGET),
        }


class RetrospectiveUserFeedbackForm(forms.ModelForm):
    class Meta:
        model = RetrospectiveUserFeedback
        exclude = ('agile_user', 'retrospective_number', 'votes')

        labels = {
            'text': 'Feedback',
            'type': 'Great or better'
        }

        widgets = {
            'type': forms.Select(attrs=SELECT_WIDGET),
            'text': forms.Textarea(attrs=TEXT_WIDGET)
        }
