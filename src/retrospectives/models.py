from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from accounts.models import Team, AgileUser

FEEDBACK_TYPES = (('better', 'better'), ('great', 'great'))


class Retrospective(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sprint_number = models.PositiveSmallIntegerField()
    slug = models.SlugField(blank=True)
    sprint_name = models.CharField(max_length=256)

    class Meta:
        unique_together = ('team', 'sprint_number',)

    def __str__(self):
        return str(self.sprint_number)


class RetrospectiveNumber(models.Model):
    sprint_number = models.ForeignKey(Retrospective, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(AgileUser, on_delete=models.CASCADE)
    fun = models.PositiveSmallIntegerField()
    value = models.PositiveSmallIntegerField()
    great = models.CharField(max_length=512, blank=True, null=True)
    better = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return str(self.sprint_number)


@receiver(pre_save, sender=Retrospective)
def save_profile(sender, instance, **kwargs):
    instance.slug = 'sprint-{}'.format(instance.sprint_number)


class RetrospectiveUserFeedback(models.Model):
    agile_user = models.ForeignKey(AgileUser, on_delete=models.CASCADE)
    retrospective_number = models.ForeignKey(RetrospectiveNumber, on_delete=models.CASCADE, related_name='feedback')
    text = models.CharField(max_length=512, blank=True, null=True)
    type = models.CharField(max_length=16, choices=FEEDBACK_TYPES)
    votes = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.text


class UserVote(models.Model):
    feedback = models.ForeignKey(RetrospectiveUserFeedback, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # TODO IS THIS CORRECT?
    voted = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=RetrospectiveUserFeedback)
def add_user_vote(sender, instance, **kwargs):
    user = User.objects.get(agile_user=instance.agile_user)
    UserVote.objects.update_or_create(
        feedback=instance, user=user,
        defaults={
            'user': user,
            'voted': True
        }
    )
