from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _
from ratelimit.decorators import ratelimit

from .forms import MyUserCreationForm, UserProfileForm
from .utils import ReCaptcha

User = get_user_model()
import logging

from django.views.decorators.clickjacking import xframe_options_exempt

logger = logging.getLogger(__name__)

@ratelimit(key='post:username', rate='10/5m')
@ratelimit(key='post:password', rate='10/5m')
@xframe_options_exempt
def rate_limit_login(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next', reverse('mapApp:index')))

    if request.limited:
        return redirect(reverse('userApp:rate_limited'))
    return LoginView.as_view(template_name='userApp/login.html')(request)

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

    # check if social account
    accounts = {}
    for account in user.socialaccount_set.all().iterator():
        providers = accounts.setdefault(account.provider, [])
        providers.append(account)
    return render(request, "userApp/profile.html", {'user': user, 'form': form, 'accounts': accounts})
