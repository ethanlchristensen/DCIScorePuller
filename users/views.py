import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Your account has been created. Please login.")
            return redirect("login")
    else:
        form = UserRegisterForm()

    context = {"form": form, "title": "Register"}
    return render(request, "users/register.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=request.user)

        old_photo = str(request.user.profile.image)

        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_update_form.is_valid() and profile_update_form.is_valid():

            user_update_form.save()
            profile_update_form.save()

            incoming_photo = profile_update_form.cleaned_data.get("image")

            if str(old_photo) != str(incoming_photo) and "profile_pics\default.png" != str(old_photo):
                os.remove(f"{settings.MEDIA_ROOT}\{old_photo}")
  
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Your profile could not be updated.")
            for key, value in user_update_form.errors.items():
                messages.error(request, value)
            for key, value in profile_update_form.errors.items():
                messages.error(request, value)
            return redirect("profile")
    else:   
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
        you = User.objects.get(username=request.user)
        context = {
            "you": you,
            "title": "Profile",
            "user_update_form": user_update_form,
            "profile_update_form": profile_update_form,
            "i_am": "profile",
        }
        return render(request, "users/profile.html", context)
