from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required
from ratelimit.decorators import ratelimit
from django.forms.utils import ErrorList

from .forms import MyUserCreationForm, UserProfileForm
from utils import ReCaptcha

from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.decorators.clickjacking import xframe_options_exempt

import logging
logger = logging.getLogger(__name__)

@ratelimit(key='post:username', rate='10/5m')
@ratelimit(key='post:password', rate='10/5m')
@xframe_options_exempt
def rate_limit_login(request):
    if request.user.is_authenticated():
        return redirect(request.GET.get('next', reverse('mapApp:index')))

    if request.limited:
        return redirect(reverse('userApp:rate_limited'))

    return auth_login(request, template_name='userApp/login.html')

def rate_limited(request):
    return render(request, 'userApp/rate_limited.html')

@xframe_options_exempt
def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        try:
            if form.is_valid():
                if ReCaptcha(request).is_valid() or settings.DEBUG:
                    # Create user
                    new_user = form.save()
                    messages.info(request, _("Thanks for registering. You are now logged in."))

                    # Log user in
                    new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
                    login(request, new_user)
                    return redirect(reverse("mapApp:index"))
                else:
                    # Google reCAPTCHA failure
                    messages.error(request, _("Captcha failure. It looks like you're a robot."))
        except KeyError as e:
            errors = form._errors.setdefault("username", ErrorList())
            errors.append(_("Username already exists."))

    else:
        form = MyUserCreationForm()

    return render(request, "userApp/register.html", {
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
            messages.info(request, _("Information updated."))
            form = UserProfileForm(instance=user)

    else:
        form = UserProfileForm(instance=user)

    return render(request, "userApp/profile.html", {'user': user, 'form': form})
