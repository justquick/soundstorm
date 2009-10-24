__docformat__ = "restructuredtext en"

from urllib import urlencode
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

class AudioPlayerNode(template.Node):
    "Renderer class for the audioplayer template tag."
    
    def __init__(self, file_url, player_url, params):
        """
        Constructor.

        Parameters:

            file_url
                The filename of the mp3 file.
            player_url
                The url of the flash based player
            params
                The parameters to pass to the flash player
        """
        self.player_url = player_url
        self.file_url = template.Variable(file_url)
        self.params = params

        # pythonify 'autostart' and 'loop'
        if self.params['autostart'].lower() == "true":
            self.params['autostart'] = "yes"
        if self.params['autostart'].lower() == "false":
            self.params['autostart'] = "no"            
        if self.params['loop'].lower() == "true":
            self.params['loop'] = "yes"
        if self.params['loop'].lower() == "false":
            self.params['loop'] = "no"
        
    def render(self, context):
        # Check if the given sound file is a template variable, otherwise use
        # the filename verbatim.
        try:
            self.params["soundFile"] =  self.file_url.resolve(context)
        except template.VariableDoesNotExist:
            self.params["soundFile"] =  self.file_url

        # urlencode the parameters for passing them to the flash app.
        # Instead of using entity &amp; use unicode &#38;        
        player_flash_params = mark_safe(urlencode(self.params).replace('&', '&#38;'))
               
        t = template.loader.get_template('audioplayer/audioplayer.html')
        # Create a new context and pass the current autocontext value to it.
        code_context = template.Context(
                            {"player_url": self.player_url,
                             "width": self.params['width'],
                             "height": self.params['height'],
                             "flash_vars": player_flash_params,
                             "bgcolor": self.params["bgcolor"].replace("0x", "#")
                            }, autoescape=context.autoescape)
        return t.render(code_context)

def do_audioplayer(parser, token):
    """
    This will insert an flash-based mp3 audioplayer in form of an <object>
    code block.

    Usage::

        {% audioplayer file=file_url %}

    The player can be customized by additional parameters. To automatically
    start playing the file in a loop using a red background color write::

        {% audioplayer file=file_url,loop=True,autostart=True,bg=0xff000 %}

    The complete list of parameters:
    
    ============== ========== ===================================================
    Parameter      Default    Description
    ============== ========== ===================================================
    file           -          The URL of the mp3 file
    playerUrl      see below  The URL of the player.swf file
    autostart      False      The player will automatically open and start to
                              play the track (False|True)
    loop           False      The track will be looped indefinitely (False|True)
    bg             0xHHHHHH   Background colour option (where HHHHHH is a valid
                              hexadecimal colour value such as FFFFFF or 009933)
    bgcolor        0xHHHHHH   Background colour
    leftbg         0xHHHHHH   Left background colour
    rightbg        0xHHHHHH   Right background colour
    rightbghover   0xHHHHHH   Right background colour (hover)
    lefticon       0xHHHHHH   Left icon colour
    righticon      0xHHHHHH   Right icon colour
    righticonhover 0xHHHHHH   Right icon colour (hover)
    text           0xHHHHHH   Text colour
    slider         0xHHHHHH   Slider colour
    loader         0xHHHHHH   Loader bar colour
    track          0xHHHHHH   Progress track colour
    border         0xHHHHHH   Progress track border colour
    width          156        The width of the player 
    height         18         The height of the player
    ============== ========== ===================================================

    By default the audioplayer tag uses the player.swf found at 
    ``{{ MEDIA_URL }}/audioplayer/player.swf``.

    To change that behaviour pass the URL of the player using the ``playerUrl``
    parameter like this::

        {% audioplayer file=file.mp3,playerUrl=/foo/bar/player.swf,loop=True %}

    """
    
    params = { "autostart": "no",
               "loop": "no",
               "bg": "0xF7F7F7",
               "bgcolor": "0xFFFFFF",
               "leftbg": "0xEFEFEF",
               "rightbg": "0xCCCCCC",
               "rightbghover": "0xAAAAAA",
               "lefticon": "0x666666",
               "righticon": "0x666666",
               "righticonhover": "0x444444",
               "text": "0x4F4F4F",
               "slider": "0xB29461",
               "loader": "0xEEFFCC",
               "track": "0xFFFFFF",
               "border": "0x00FF00",               
               "width": "156",
               "height": "18"
             }
    
    player_url = "%s/audioplayer/player.swf" % (settings.MEDIA_URL)
    file_url = str()
    
    try:
        # token has the form "audioplayer param=value,param=value,..."
        tag, tag_params = token.split_contents()
        
        # tag_params now has the form:
        # 'file=/media/audio/song.mp3,autostart=False,loop=False,bgcolor=0xBAFF7B'
        
        for t in tag_params.split(','):
            # each param has the form key=value, so we first split them
            keyAndValue = t.split("=")
            if len(keyAndValue)!=2:                                
                raise template.TemplateSyntaxError, "Error splitting tag param %r. Format should be: key=value" % t
            else:
                key, value = keyAndValue[0], keyAndValue[1]                                
                if params.has_key(key):
                    params[key] = value;
                else:
                    # The 'playerUrl' is a parameter which is not passed to
                    # the player thus it is handled differently
                    if key == "playerUrl":
                        player_url = value
                    if key == "file":
                        file_url = value                                    
                    if not key:
                        raise template.TemplateSyntaxError, "Unknown parameter %s in template tag audioplayer. Available params: %s" % (key, params)                                                
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
       
    return AudioPlayerNode(file_url, player_url, params)


# register the tag 
register.tag('audioplayer', do_audioplayer)

