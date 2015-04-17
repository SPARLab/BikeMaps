from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^forum/', include('spirit.urls', namespace="spirit", app_name="spirit")),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /experimental", mimetype="text/plain"))
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
