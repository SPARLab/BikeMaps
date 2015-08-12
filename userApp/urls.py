from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from userApp import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^login/$', views.rate_limit_login, name='login'),
    url(r'^rate_limited/$', views.rate_limited, name='rate_limited'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'userApp/logged_out.html', 'next_page': '/'}, name='logout'),

    url(r'^password_change/$', 'django.contrib.auth.views.password_change',{'template_name': 'userApp/password_change_form.html', 'post_change_redirect': reverse_lazy('userApp:password_change_done')}, name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',{'template_name': 'userApp/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',{'template_name': 'userApp/password_reset_form.html', 'email_template_name': 'userApp/password_reset_email.html', 'post_reset_redirect': reverse_lazy('userApp:password_reset_done')}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'userApp/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm',{'template_name': 'userApp/password_reset_confirm.html', 'post_reset_redirect': reverse_lazy('userApp:password_reset_complete')}, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'userApp/password_reset_complete.html'}, name='password_reset_complete'),
]
