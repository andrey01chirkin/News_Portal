from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from models_app.models import Author


@login_required
def upgrade_me(request):
    user = request.user
    if not Author.objects.filter(user=request.user).exists():
        Author.objects.create(user=request.user)

    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)

    return redirect('/news/')