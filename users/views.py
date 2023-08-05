from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.conf import settings
import os


def register(request):
    if request.method == "POST":
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            f = form.save()
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
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_update_form.is_valid() and profile_update_form.is_valid():
            old_photo = User.objects.filter(id=request.user.id).first().profile.image

            user_update_form.save()
            profile_update_form.save()

            incoming_photo = profile_update_form.cleaned_data["image"]

            if str(old_photo) not in str(incoming_photo) and "default.png" not in str(
                old_photo
            ):
                os.remove(f"{settings.MEDIA_ROOT}\{old_photo}")

            messages.success(request, "Your profile has been updated successfully.")
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
            "i_am": "profile"
        }
    return render(request, "users/profile.html", context)
