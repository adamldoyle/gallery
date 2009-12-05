from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'gallery.views.default'),
    (r'^(?P<gallery_id>\d+)/$', 'gallery.views.view_gallery'),
    (r'^(?P<slug>[-\w]+)/$', 'gallery.views.view_gallery'),
)
