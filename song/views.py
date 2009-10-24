from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.template import Context,Template
from soundstorm.song.models import Song
from urllib import quote
from django.template import RequestContext
import os

#def download(request, song_id):
#    song = get_object_or_404(Song, pk = song_id)
#    content = open(song.filename,'rb').read()
#    response = HttpResponse(content, mimetype = song.mime_type)
#    response["Content-Disposition"] = "attachment; filename=%s"%\
#        quote(os.path.basename(song.filename)).replace('%20','_')
#    response["Content-Length"] = len(content)
#    return response

def player(request, song_id):
    song = get_object_or_404(Song, pk = song_id)
    return render_to_response('player.html',{'url':'/songs/download/%s/'%song_id})

def info(request, song_id):
    ctx = Context({'song': get_object_or_404(Song, pk = song_id)})
    return HttpResponse(Template("""
    <ul>{% if song.duration %}<li><b>Length:</b> {{ song.duration }}</li>{% endif %}
    <li>{% if song.music_genre %}<b>Genre:</b> {{ song.music_genre }}</li>{% endif %}
    <li>{% if song.track_number %}<b>Track Number:</b> {{ song.track_number }}</li>{% endif %}
    <li>{% if song.sample_rate %}<b>Sample Rate:</b> {{ song.sample_rate }}</li>{% endif %}
    <li>{% if song.bit_rate %}<b>Bit Rate:</b> {{ song.bit_rate }}</li>{% endif %}
    <li>{% if song.format_version %}<b>Format:</b> {{ song.format_version }}</li>{% endif %}
    <li>{% if song.mime_type %}<b>Mime Type:</b> {{ song.mime_type }}</li>{% endif %}</ul>
    <a href="javascript:close_info("""+song_id+""");">close</a>""").render(ctx))
    

def list(request):
    songs = Song.objects.all()
    order = None
    if 'order' in request.GET:
        order = request.GET['order']
        songs = songs.order_by(order)
    return render_to_response('list.html', {'songs':songs,'order':order}, 
        context_instance = RequestContext(request))

def browse(request, path):
    songs = Song.objects.all()
    order = None
    crumbs = [('/songs/browse/','Home')]
    if not path: dirs = map(lambda x: (os.path.basename(x),os.path.basename(x)), settings.SONG_DIRS)
    else:
        for dir in settings.SONG_DIRS:
            if path.startswith(os.path.basename(dir)):
                for part in path.split('/')[1:]:
                    dir = os.path.join(dir, part)
                    print ( '%s/%s'%(crumbs[-1][0],part), part )
                    crumbs.append(( '%s/%s'%(crumbs[-1],part), part ))
                dirs = [(x,'%s/%s'%(path,x)) for x in os.listdir(dir) if os.path.isdir(os.path.join(dir,x))]
                songs = songs.filter(filename__startswith=dir)

    if 'order' in request.GET:
        order = request.GET['order']
        songs = songs.order_by(order)
        
    return render_to_response('browse.html', {'songs':songs,'dirs':dirs,'order':order}, 
        context_instance = RequestContext(request))