import re
import os

from piston.handler import BaseHandler
from piston.utils import rc, throttle
from django.conf import settings

from models import Song

class DirectoryHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        path = request.path.replace('/api/dirs/','')       
        dirs =  map(lambda x: (os.path.basename(x),os.path.basename(x)), settings.SONG_DIRS)
        if path:
            for dir in settings.SONG_DIRS:
                if path.startswith(os.path.basename(dir)):
                    dirs = [(x,'%s/%s'%(path,x)) for x in os.listdir(dir) if os.path.isdir(os.path.join(dir,x)) and not x.startswith('.')]
                    break
        return dirs        

class SongHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Song
    fields = map(lambda x: x.name, Song._meta.fields)

    #@classmethod
    #def content_size(self, song):
    #    return len(song.content)

    def read(self, request):
        songs = Song.objects.all()
        path = request.path.replace('/api/songs/','')
        if path:
            for dir in settings.SONG_DIRS:
                name = os.path.basename(dir)
                if path.startswith(name):
                    trans = str(dir+path).replace('%s/' % name, '/')
                    print trans
                    songs = songs.filter(filename__startswith=trans)
                    break
    
        if 'order' in request.GET:
            songs = songs.order_by(request.GET['order'])
        
        return songs[int(request.GET.get('offset',0)):int(request.GET.get('offset',20))]
                    
        
    ##@throttle(5, 10*60) # allow 5 times in 10 minutes
    #def update(self, request, slug):
    #    post = Song.objects.get(slug=post_slug)
    #
    #    post.title = request.PUT.get('title')
    #    post.save()
    #
    #    return post
    #
    #def delete(self, request, post_slug):
    #    post = song.objects.get(slug=post_slug)
    #
    #    if not request.user == post.author:
    #        return rc.FORBIDDEN # returns HTTP 401
    #
    #    post.delete()
    #
    #    return rc.DELETED # returns HTTP 204
