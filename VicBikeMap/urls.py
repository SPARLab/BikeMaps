from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mapApp.urls', namespace="mapApp")),
    url(r'^blog/', include('blogApp.urls', namespace="blogApp")),
    url(r'^forum/', include('spirit.urls', namespace="spirit", app_name="spirit")),
    (r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
