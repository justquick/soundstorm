from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    (r'^admin/(.*)', admin.site.root),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^api/', include('song.urls')),
    (r'', 'django.views.generic.simple.direct_to_template', {'template':'index.html'}),
    #(r'^$', include('song.urls')),
)
