from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.i18n import javascript_catalog
from django.contrib import admin
admin.autodiscover()
js_info_dict = {
    'domain': "djangojs",
    'packages': ('BikeMaps','mapApp',),
}

urlpatterns = patterns('',
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^user/', include('userApp.urls', namespace="userApp"), {'SSL':True}),
    url(r'^blog/', include('blogApp.urls', namespace="blogApp")),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^admin/', include(admin.site.urls)),

    (r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

	url(r'^jsi18n/$', javascript_catalog, js_info_dict),
)

# Add internationalization url patters to these pages
urlpatterns += i18n_patterns('',
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^user/', include('userApp.urls', namespace="userApp")),
    url(r'^blog/', include('blogApp.urls', namespace="blogApp")),
	url(r'^jsi18n/$', javascript_catalog, js_info_dict),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
