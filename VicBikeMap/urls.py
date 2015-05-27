from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^blog/', include('blogApp.urls', namespace="blogApp")),
    url(r'^forum/', include('spirit.urls', namespace="spirit", app_name="spirit")),

    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', }), #Override next page to go to home
    url('^', include('django.contrib.auth.urls')),

    (r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
