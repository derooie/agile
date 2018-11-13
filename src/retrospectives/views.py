from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

from accounts.models import AgileUser
from retrospectives.forms import AddRetrospectiveValuesForm, RetrospectiveUserFeedbackForm
from retrospectives.models import Retrospective, RetrospectiveNumber, RetrospectiveUserFeedback, UserVote


def get_team(user):
    agile_user = AgileUser.objects.get(user=user)
    return agile_user.team


class IndexView(LoginRequiredMixin, ListView):
    model = Retrospective
    template_name = 'retrospectives/index.html'

    def get_context_data(self, **kwargs):
        retros = Retrospective.objects.filter(team=get_team(self.request.user)).order_by('sprint_number')

        # Building graph data
        agile_user = AgileUser.objects.get(user__username=self.request.user.username)
        graph_data = {}
        graph_values = []
        for retro in retros:
            data = retro.retrospectivenumber_set.all()
            fun = data.aggregate(Avg('fun'))
            value = data.aggregate(Avg('value'))
            graph_values.append({
                'fun': fun.get('fun__avg'),
                'value': value.get('value__avg'),
                'sprint_number': 'sprint {}'.format(retro.sprint_number)
            })
        graph_data['graph_values'] = graph_values
        graph_data['chart_type'] = agile_user.chart_type

        return {'retrospectives': retros.order_by('-sprint_number'), 'graph_data': graph_data,
                'page_tile': 'Retrospectives overview'}


class RetrospectiveDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'retrospectives/details.html'

    def __init__(self):
        self.slug = None
        self.team = None
        self.agile_user = None
        self.user = None
        self.sprint = None
        self.sprint_number = None
        self.retrospective_numbers = None
        self.details = None
        super(RetrospectiveDetailsView, self).__init__()

    def dispatch(self, request, *args, **kwargs):
        """
        Finding all values needed later for context
        """
        self.user = self.request.user
        self.agile_user = AgileUser.objects.get(user=self.user)
        self.team = get_team(self.request.user)
        self.slug = self.kwargs['slug']

        # If sprint does not exists redirect to retrospectives index
        try:
            self.sprint_number = Retrospective.objects.get(slug=self.slug, team=self.team)
        except Retrospective.DoesNotExist:
            messages.error(request, 'The sprint you wanted to goto does not exist.')
            return HttpResponseRedirect(reverse('retrospectives:index'))

        self.details = RetrospectiveNumber.objects.filter(team=self.team, sprint_number=self.sprint_number)

        self.retrospective_numbers = RetrospectiveNumber.objects.filter(team=self.team,
                                                                        sprint_number=self.sprint_number)

        # If user has not submitted feedback redirect to adding values
        if not self.retrospective_numbers:
            return HttpResponseRedirect(reverse('retrospectives:add_values', kwargs={'slug': self.slug}))

        return super(RetrospectiveDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # Build a list of users who gave sprint feedback
        users = {}
        for user in self.retrospective_numbers:
            users[user.user] = user.user

        # Start building a feedback object which will be passed as context with feedback per user
        feedback_obj = []
        for user in users:
            user_feedback_list = []
            user_feedback = RetrospectiveUserFeedback.objects.filter(agile_user__team=self.team,
                                                                     agile_user=user,
                                                                     retrospective_number__sprint_number=self.sprint_number).order_by(
                '-votes')

            for feedback in user_feedback:
                user_feedback_list.append(
                    {'type': feedback.type, 'text': feedback.text, 'votes': feedback.votes, 'pk': feedback.pk,
                     'slug': self.slug}
                )

            feedback_obj.append({'user': user.user.username, 'feedback': user_feedback_list})

        # Build data for graph
        # retros = Retrospective.objects.filter(team=get_team(self.request.user)).order_by('-sprint_number')
        graph_data = {}
        graph_values = []
        for retro in self.details:
            graph_values.append(
                {
                    'user': retro.user.user.username,
                    'fun': retro.fun,
                    'value': retro.value,
                },
            )
        graph_data['graph_values'] = graph_values
        graph_data['chart_type'] = self.agile_user.chart_type

        return {
            'details': self.details, 'slug': self.slug, 'feedback_pk': self.sprint_number, 'graph_data': graph_data,
            'page_tile': 'Retrospective details ', 'sprint_name': self.sprint_number.sprint_name,
            'feedback_obj': feedback_obj
        }


class AddRetrospectiveNumberView(LoginRequiredMixin, CreateView):
    template_name = 'retrospectives/update_values.html'
    form_class = AddRetrospectiveValuesForm
    success_url = '/retrospectives/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.team = get_team(user)
        form.instance.user = AgileUser.objects.get(user=user)
        form.instance.sprint_number = Retrospective.objects.get(team=get_team(self.request.user),
                                                                slug=self.kwargs['slug'])
        form.save()
        messages.success(self.request, 'Values saved')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was a problem submitting the form')
        return super().form_invalid(form)


class UpdateRetrospectiveNumberView(LoginRequiredMixin, UpdateView):
    form_class = AddRetrospectiveValuesForm
    template_name = 'retrospectives/update_values.html'
    model = RetrospectiveNumber

    def get_success_url(self):
        print(self.kwargs)
        retrospective_number_pk = self.kwargs.get('pk')
        retrospective = RetrospectiveNumber.objects.get(pk=retrospective_number_pk)
        sprint = Retrospective.objects.get(sprint_number=retrospective.sprint_number.sprint_number,
                                           team=get_team(self.request.user))
        return '/retrospectives/{}/'.format(sprint.slug)

    def get_context_data(self, **kwargs):
        context = super(UpdateRetrospectiveNumberView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Values updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'There was a problem submitting the form')
        return super().form_invalid(form)


def vote(request, feedback_pk, slug):
    # Checking if user already voted on this feedback
    feedback = RetrospectiveUserFeedback.objects.get(pk=feedback_pk)
    obj, created = UserVote.objects.update_or_create(
        feedback=feedback, user=request.user,
        defaults={
            'voted': True,
        }
    )
    # If user did not already voted, a combination user/feedback will be created in UserVote table hence created
    # will be True. If created is True the amount of votes for the feedback will be updated with plus one.
    if created:
        feedback.votes += 1
        feedback.save()
    else:
        messages.warning(request, 'You are the creator of this point or already voted')
    return HttpResponseRedirect('/retrospectives/{}/'.format(slug))


class RetrospectiveUserFeedbackView(CreateView):
    form_class = RetrospectiveUserFeedbackForm
    success_url = '/retrospectives/feedback/'
    model = RetrospectiveUserFeedback
    template_name = 'retrospectives/feedback.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        retrospective_number = RetrospectiveNumber.objects.get(pk=self.kwargs.get('pk'))
        retrospective = Retrospective.objects.get(pk=retrospective_number.sprint_number.pk)
        return '/retrospectives/{}/'.format(retrospective.slug)

    def form_valid(self, form):
        feedback_pk = self.kwargs.get('pk')
        agile_user = AgileUser.objects.get(user__username=self.request.user.username)
        form.instance.agile_user = agile_user
        form.instance.retrospective_number = RetrospectiveNumber.objects.get(pk=feedback_pk)
        return super().form_valid(form)
