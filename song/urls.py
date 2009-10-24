from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from handlers import SongHandler, DirectoryHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

song_resource = Resource(handler=SongHandler, **ad)
dir_resource = Resource(handler=DirectoryHandler, **ad)

urlpatterns = patterns('',
    url(r'^songs/', song_resource, { 'emitter_format': 'json' }), 
    url(r'^dirs/', dir_resource, { 'emitter_format': 'json' }), 
)