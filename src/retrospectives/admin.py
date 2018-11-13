from django.contrib import admin

from retrospectives.models import Retrospective, RetrospectiveNumber, RetrospectiveUserFeedback, UserVote


class RetrospectiveUserFeedbackInline(admin.StackedInline):
    model = RetrospectiveUserFeedback
    extra = 1


class RetrospectiveAdmin(admin.ModelAdmin):
    list_display = ['sprint_number', 'team', 'sprint_name']


class RetrospectiveNumberAdmin(admin.ModelAdmin):
    inlines = [RetrospectiveUserFeedbackInline]
    list_display = ['team', 'sprint_number', 'user']


class RetrospectiveUserFeedbackAdmin(admin.ModelAdmin):
    # inlines = [BetterInputInline]
    list_display = ['agile_user', 'retrospective_number',  'text']


class UserVoteAdmin(admin.ModelAdmin):
    list_display = ['user','feedback','voted']


admin.site.register(Retrospective, RetrospectiveAdmin)
admin.site.register(RetrospectiveNumber, RetrospectiveNumberAdmin)
admin.site.register(RetrospectiveUserFeedback, RetrospectiveUserFeedbackAdmin)
admin.site.register(UserVote, UserVoteAdmin)
