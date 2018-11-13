from accounts.models import AgileUser


# Get team where user is member of
def get_team(request):
    if request.user.is_authenticated:
        try:
            agile_user = AgileUser.objects.get(user=request.user)
            return {'team': agile_user.team}
        except AgileUser.DoesNotExist:
            return {'team': None}
    else:
        return {'team': None}
