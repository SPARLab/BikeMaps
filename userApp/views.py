from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import MyUserCreationForm, UserProfileForm
from utils import ReCaptcha

from django.contrib.auth import get_user_model
User = get_user_model()

import logging
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            if ReCaptcha(request).is_valid():
                # Create user
                new_user = form.save()
                messages.info(request, "Thanks for registering. You are now logged in.")

                # Log user in
                new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
                login(request, new_user)
                return redirect(reverse("mapApp:index"))
            else:
                # Google reCAPTCHA failure
                messages.danger(request, "Captcha failure. It looks like you're a robot.")
    else:
        form = MyUserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })

@login_required
def profile(request):
    user = get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=user)

        if form.is_valid():
            form.save(commit=False)
            user.save()
            messages.info(request, "Information updated.")
            form = UserProfileForm(instance=user)

    else:
        form = UserProfileForm(instance=user)

    return render(request, "userApp/profile.html", {'user': user, 'form': form})
