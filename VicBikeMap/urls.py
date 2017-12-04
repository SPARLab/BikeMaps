from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.i18n import JavaScriptCatalog
from django.contrib import admin
from solid_i18n.urls import solid_i18n_patterns
from rest_framework.authtoken import views as auth_views
from django.views import static
import certbot_django.server.urls

admin.autodiscover()
js_info_dict = {
    'domain': "djangojs",
    'packages': ('BikeMaps','mapApp',),
}



urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# Add internationalization url patters to these pages
urlpatterns += solid_i18n_patterns(
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^user/', include('userApp.urls', namespace="userApp")),
    url(r'^blog/', include('blogApp.urls', namespace="blogApp")),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    ]
