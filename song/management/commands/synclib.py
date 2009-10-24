from django.core.management.base import BaseCommand  
from soundstorm.song.models import Song
from django.conf import settings
from sys import stderr
import threading
import os

try:
    from hachoir_core.error import HachoirError
    from hachoir_core.cmd_line import unicodeFilename
    from hachoir_parser import createParser
    from hachoir_core.tools import makePrintable
    from hachoir_metadata import extractMetadata
    from hachoir_core.i18n import getTerminalCharset
except ImportError:
    raise ImportError, 'You need to have the hachoir core,parser and metadata libraries installed'

COLS = ('title', 'author', 'album', 'duration', 'music_genre', 'track_number', 'sample_rate', 'bit_rate', 'format_version', 'mime_type')

def is_song(filename):
    return os.path.splitext(filename)[1] in settings.SONG_TYPES

def stat(filename):
    stat = os.stat(filename)
    return '%s.%s' % (stat.st_size, stat.st_mtime)
    
def has_changed(song):
    return song.stat and song.stat != stat(song.filename)

class Walk(threading.Thread):
    def __init__(self, adir):
        self.adir = adir
        threading.Thread.__init__(self)
        
    def run(self):
        for filename in os.listdir(self.adir):
            filename = os.path.join(self.adir, filename)
            if os.path.isdir(filename):
                while 1:
                    try:
                        Walk(filename).start()
                        break
                    except:
                        continue
                        
            elif os.path.isfile(filename) and is_song(filename):
                filename, realname = unicodeFilename(filename), filename
                try:
                    song = Song.objects.get(filename = filename)
                except:
                    song = Song(filename = filename, name = os.path.splitext(os.path.basename(filename))[0])  
                if not has_changed(song):
                    continue
                song.stat = stat(filename)
                try:
                    parser = createParser(filename, realname)
                except:
                    parser = None
                if not parser:
                    print >>stderr, "Unable to parse file %s"%filename
                    continue 
                try:
                    metadata = extractMetadata(parser)
                except HachoirError, err:
                    print >>stderr, "Metadata extraction error: %s" % unicode(err)
                    continue
                if not metadata:
                    print >>stderr, "Unable to extract metadata"
                    continue
                else:
                    text = metadata.exportPlaintext()
                    charset = getTerminalCharset()
                    for line in text[1:]:
                        line = makePrintable(line, charset)
                        key = line[2:].split(': ')[0].replace(' ','_').replace('/','_').lower()
                        if key in COLS:
                            setattr(song,key,line[len(key)+4:])
                while 1:
                    try:
                        song.save()
                        break
                    except:
                        continue

class Command(BaseCommand):  
    help = "Syncs your collection of songs into the database."  
    def handle(self, *args, **options):
        threads = threading.activeCount()  
        for DIR in settings.SONG_DIRS:
            Walk(DIR).start()
        while threading.activeCount() > threads:
            continue