from django.contrib import admin

from accounts.models import AgileUser, Team


class AgileUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', ]


admin.site.register(AgileUser, AgileUserAdmin)
admin.site.register(Team)
