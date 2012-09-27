#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Providers configuration.

List here the video providers that should be used to match a video.

"""

PROVIDERS = {
    'youtube': {
        'link_template': r"""http://www.youtube.com/embed/{video_id}""",
        'embed_template': r"""<iframe width="560" height="315" src="{video_link}" frameborder="0" allowfullscreen></iframe>""",
        'validation_template': r"""http://www.youtube.com/watch?v={video_id}""",
        'matches': [
            r"""youtube.[^/]+/v/([^"'/&?@]+)""",
            r"""youtube.[^/]+/embed/([^"'/&?@]+)""",
        ]
    },
    'vimeo': {
        'link_template': r"""http://player.vimeo.com/video/{video_id}""",
        'embed_template': r"""<iframe src="{video_link}" width="480" height="372" frameborder="0"></iframe>""",
        'validation_template': r"""http://vimeo.com/{video_id}""",
        'matches': [
            r"""vimeo.[^/]+/video/([^"'/&?@]+)""",
        ]
    },
    'google': {
        'link_template': r"""http://video.google.com/googleplayer.swf?docId={video_id}""",
        'embed_template': r"""<embed id=VideoPlayback src="{video_link}" style="width:400px;height:326px" allowFullScreen=true allowScriptAccess=always type=application/x-shockwave-flash> </embed>""",
        'validation_template': r"""http://video.google.com/videoplay?docid={video_id}""",
        'matches': [
            r"""video.google.[^/]+/googleplayer.swf\?docId=([^"'/&?@]+)""",
        ]
    },
    'dailymotion': {
        'link_template': r"""http://www.dailymotion.com/embed/video/{video_id}""",
        'embed_template': r"""<iframe frameborder="0" width="480" height="270" src="{video_link}"></iframe>""",
        'validation_template': r"""http://www.dailymotion.com/video/{video_id}""",
        'matches': [
            r"""dailymotion.[^/]+/swf/([^"'/&?@]+)""",
            r"""dailymotion.[^/]+/embed/video/([^"'/&?@]+)""",
        ]
    },
    'crosstv': {
        'link_template': r"""http://embed.cdn01.net/player.php?width=640&height=360&tvButtonID=crosstv&id={video_id}""",
        'embed_template': r"""<iframe src='{video_link}' frameborder='0' width='640' height='360'></iframe>""",
        'validation_template': r"""http://embed.cdn01.net/player.php?width=640&height=360&tvButtonID=crosstv&id={video_id}""",
        'matches': [
            r"""embed.cdn01.[^/]+/player.php\?.*?&id=([^"'/&?@]+)""",
            r"""flashvars='.*?id=([^"'/&?@]+).*?tvButtonID=crosstv""",
        ]
    },
}
