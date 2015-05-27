from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages
from .forms import MyUserCreationForm
import requests

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


class ReCaptcha:
    def __init__(self, request):
        params = {
            'secret': settings.RECAPTCHA_SECRET,
            'response': request.POST.get('g-recaptcha-response'),
            'remoteip': request.META['REMOTE_ADDR']
        }
        self.response = requests.get('https://www.google.com/recaptcha/api/siteverify', params=params).json()

    def is_valid(self):
        return self.response['success']
