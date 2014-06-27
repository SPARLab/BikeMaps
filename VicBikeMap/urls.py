from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^spirit/', include('spirit.urls', namespace="spirit", app_name="spirit")),
)
