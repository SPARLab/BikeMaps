from django.conf.urls import url, include
from django.urls import reverse_lazy
from userApp import views
from django.contrib.auth import views as django_contrib_auth_views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^login/$', views.rate_limit_login, name='login'),
    url(r'^rate_limited/$', views.rate_limited, name='rate_limited'),
    url(r'^logout/$', django_contrib_auth_views.LogoutView.as_view( template_name='userApp/logged_out.html', next_page= '/' ), name='logout'),
    url(r'^password_change/$', django_contrib_auth_views.PasswordChangeView, {'template_name': 'userApp/password_change_form.html', 'post_change_redirect': reverse_lazy('userApp:password_change_done')}, name='password_change'),
    url(r'^password_change/done/$', django_contrib_auth_views.PasswordChangeDoneView, {'template_name': 'userApp/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset/$', django_contrib_auth_views.PasswordResetView, {'template_name': 'userApp/password_reset_form.html', 'email_template_name': 'userApp/password_reset_email.html', 'post_reset_redirect': reverse_lazy('userApp:password_reset_done')}, name='password_reset'),
    url(r'^password_reset/done/$', django_contrib_auth_views.PasswordResetDoneView, {'template_name': 'userApp/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', django_contrib_auth_views.PasswordResetConfirmView, { 'template_name': 'userApp/password_reset_confirm.html', 'post_reset_redirect': reverse_lazy('userApp:password_reset_complete')}, name='password_reset_confirm'),
    url(r'^reset/done/$', django_contrib_auth_views.PasswordResetCompleteView, {'template_name': 'userApp/password_reset_complete.html'}, name='password_reset_complete'),
]
