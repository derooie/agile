from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

CHART_CHOICES = (("column", "Column"), ("line", "Line"))


class Team(models.Model):
    team_name = models.CharField(max_length=128)

    def __str__(self):
        return self.team_name


class AgileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agile_user')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    chart_type = models.CharField(max_length=16, default='column', choices=CHART_CHOICES)

    def __str__(self):
        return self.user.username
