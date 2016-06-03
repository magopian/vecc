#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Providers configuration.

List here the video providers that should be used to match a video.

"""

LIVE_PROVIDERS = {
    'youtube': {
        'link_template': '//www.youtube.com/embed/'
                         '{video_id}?autoplay=1&rel=0',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://www.youtube.com/watch?v={video_id}',
        'matches': [
            r"""youtube.[^/]+/watch\?[^v]*v\=([^"'/&?@]+)""",
            r"""youtu.be/([^"'/&?@]+)""",
            r"""youtube.[^/]+/v/([^"'/&?@]+)""",
            r"""youtube.[^/]+/embed/([^"'/&?@]+)""",
        ]
    },
    'creacast': {
        'link_template': 'http://www.creacast.com/'
                         '{video_id}',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://www.creacast.com/{video_id}',
        'matches': [
            r"""creacast.[^/]+/([^"'/]+)""",
        ]
    },
    'piksel': {
        'link_template': 'http://player.piksel.com/'
                         '{video_id}',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://player.piksel.com/{video_id}',
        'matches': [
            r"""piksel.[^/]+/([^"'/]+)""",
        ]
    },
    'lightcastmedia': {
        'link_template': 'http://{video_id}',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': '{video_id}',
        'matches': [
            r"""([a-zA-Z0-9]+\.lightcastmedia.[^/]+/.+)""",
        ]
    },
}


PROVIDERS = {
    'youtube': {
        'link_template': '//www.youtube.com/embed/'
                         '{video_id}?autoplay=1&rel=0',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://www.youtube.com/watch?v={video_id}',
        'matches': [
            r"""youtube.[^/]+/watch\?[^v]*v\=([^"'/&?@]+)""",
            r"""youtu.be/([^"'/&?@]+)""",
            r"""youtube.[^/]+/v/([^"'/&?@]+)""",
            r"""youtube.[^/]+/embed/([^"'/&?@]+)""",
        ]
    },
    'vimeo': {
        'link_template': '//player.vimeo.com/'
                         'video/{video_id}?autoplay=1',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://vimeo.com/{video_id}',
        'matches': [
            r"""vimeo.[^/]+/video/([^"'/&?@]+)""",
            r"""vimeo.[^/]+/moogaloop.swf\?clip_id=([^"'/&?@]+)""",
            r"""vimeo.[^/]+/[a-z]+/([^a-z"'/&?@]+)""",
            r"""vimeo.[^/]+/[a-z]+/[a-z]+/([^a-z"'/&?@]+)""",
            r"""vimeo.[^/]+/([^"'/&?@]+)""",
        ]
    },
    'google': {
        'link_template': '//video.google.com/googleplayer.swf?'
                         'docId={video_id}&autoPlay=1&related=0',
        'embed_template': '<embed id=VideoPlayback src="{video_link}" '
                          'style="width:480px;height:395px" '
                          'allowfullscreen="true" '
                          'allowScriptAccess=always '
                          'type=application/x-shockwave-flash> </embed>',
        'validation_template': 'http://video.google.com/videoplay?'
                               'docid={video_id}',
        'matches': [
            r"""video.google.[^/]+/googleplayer.swf\?docId=([^"'/&?@]+)""",
        ]
    },
    'dailymotion': {
        'link_template': '//www.dailymotion.com/embed/video/{video_id}?'
                         'autoPlay=1&related=0',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://www.dailymotion.com/video/{video_id}',
        'matches': [
            r"""dailymotion.[^/]+/swf/video/([^"'/&?@]+)""",
            r"""dailymotion.[^/]+/swf/([^"'/&?@]+)""",
            r"""dailymotion.[^/]+/embed/video/([^"'/&?@]+)""",
            r"""dailymotion.[^/]+/video/([^"'/&?@]+)_.*""",
            r"""dai.ly/([^"'/&?@]+)""",
        ]
    },
    'crosstv': {
        'link_template': '//embed.cdn01.net/player.php?width=640&'
                         'height=360&tvButtonID=crosstv&autoPlay=1&'
                         'related=0&id={video_id}',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'http://embed.cdn01.net/player.php?width=640&'
                               'height=360&tvButtonID=crosstv&id={video_id}',
        'matches': [
            r"""embed.cdn01.[^/]+/player.php\?.*?&id=([^"'/&?@]+)""",
            r"""flashvars='.*?id=([^"'/&?@]+).*?tvButtonID=crosstv""",
        ]
    },
    'facebook': {
        'link_template': '//www.facebook.com/video/embed?video_id={video_id}',
        'embed_template': '<iframe width="480" height="395" '
                          'src="{video_link}" frameborder="0"></iframe>',
        'validation_template': 'https://www.facebook.com/video.php?v='
                               '{video_id}',
        'matches': [
            r"""facebook.[^/]+/video.php\?[^v]*v\=([^"'/&?@]+)""",
            r"""facebook.[^/]+/video/embed\?video_id\=([^"'/&?@]+)""",
            r"""facebook.[^/]+/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/([^"'/&?@]+)""",
        ]
    },
}
