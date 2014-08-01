from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^forum/', include('spirit.urls', namespace="spirit", app_name="spirit")),
)

# urlpatterns += patterns('',
#     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
# )