from soundstorm.song.models import Song
from django.contrib import admin

class SongAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','filename']}),
        ('Meta information', {'fields': ['title', 'author', 'album', 'duration', 'music_genre', 'track_number', 'sample_rate', 'bit_rate', 'format_version', 'mime_type']}),
    ]
    list_display = ('name','title', 'author', 'album', 'duration', 'music_genre', 'track_number', 'sample_rate', 'bit_rate', 'format_version', 'mime_type')


admin.site.register(Song, SongAdmin)
