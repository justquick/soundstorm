from django.db.models import *
from django.template.defaultfilters import slugify

class Song(Model):
    filename = TextField()
    name =  CharField(max_length = 255)
    slug = SlugField()
    title = CharField(max_length = 255, blank = True, null = True)
    author = CharField(max_length = 255, blank = True, null = True) 
    album = CharField(max_length = 255, blank = True, null = True)
    duration = CharField(max_length = 255, blank = True, null = True)
    music_genre = CharField(max_length = 255, blank = True, null = True)
    track_number = IntegerField(blank = True, null = True) 
    sample_rate  = CharField(max_length = 255, blank = True, null = True)
    bit_rate = CharField(max_length = 255, blank = True, null = True)
    format_version = CharField(max_length = 255, blank = True, null = True)
    mime_type = CharField(max_length = 255, blank = True, null = True)
    stat = CharField(max_length = 255, blank = True, null = True)
    
    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Song, self).save(*a, **kw)
        
    def __unicode__(self): return self.name
    
