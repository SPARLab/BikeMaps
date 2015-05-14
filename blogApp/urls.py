from django.conf.urls import patterns, url
from blogApp import views

urlpatterns = patterns('',
	# Index page
	url(r'^$', views.index, name='index'),

	# View a post
	url(r'^post/(?P<slug>[\w\-]+)$', views.view_post, name='view_post'),

	url(r'^p/(?P<s62>[\w]+)$', views.short_url_redirect, name='short_url_redirect'),

	# Create a post
	url(r'^create/$', views.create_post, name='create_post'),

	# Edit a post
	url(r'^edit/(?P<slug>[\w\-]+)$', views.edit_post, name='edit_post'),

	# Upload image url
	url(r'^upload_image/$', views.upload_image, name='upload_image'),
)
