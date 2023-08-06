from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

@staff_member_required
def wipe_users(request):
    User.objects.all().delete()
    return redirect("pull-home")