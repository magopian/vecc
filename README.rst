########################
Video Embed Code Cleaner
########################

Cleans and updates your video's embed code.

Over time, the embed codes used for videos from various providers have changed
and evolved, to make them more and more compatible with a broader set of
devices.

This is where vecc is useful: it detects the video provider and id from a given
embed code, and provides various utilities to clean this code and validate that
the video is still available.


Install
=======

Either use ``pip``, which is the easiest way:

::

    $ pip install vecc

Either download the tarball from http://pypi.python.org/pypi/vecc, untar it,
and install it manually:

::

    $ python setup.py install


Usage
=====

::

    $ vecc -h
    usage: vecc [-h] [--version] {clean,validate} ...

    Video Embed Code Cleaner.

    optional arguments:
      -h, --help        show this help message and exit
      --version         show program's version number and exit

    sub-commands:
      {clean,validate}
        clean           clean the embed code
        validate        validate that the video is still available


Sub-commands
============

* ``clean``: takes a video embed code, and returns the video id, provider, and
  new embed code. Takes an optional ``-v|--validate`` parameter, to check if
  the video is still available.
* ``validate``: takes a video id and provider, and check if it's still
  available.


Example
=======

::

    $ vecc clean '<object width="480" height="381"><param name="movie" value="http://www.dailymotion.com/swf/k6Lg9UXest3kho5p9X&related=0"></param><param name="allowFullScreen" value="true"></param><param name="allowScriptAccess" value="always"></param><embed src="http://www.dailymotion.com/swf/k6Lg9UXest3kho5p9X&related=0" type="application/x-shockwave-flash" width="480" height="381" allowFullScreen="true" allowScriptAccess="always"></embed></object>' -v
    video id: k6Lg9UXest3kho5p9X
    provider: dailymotion
    embed code: <iframe frameborder="0" width="480" height="270" src="http://www.dailymotion.com/embed/video/k6Lg9UXest3kho5p9X"></iframe>
    This video is still valid


Providers
=========

Video providers (Google video, Youtube, Vimeo, Dailymotion...) are configured
in the ``vecc/providers.py`` file.

Each provider configuration consists of:

* name: youtube
* link template: string template (that'll be interpolated with format_) used to
  build the cleaned code. This is the link to the embedded video player. Needs
  the ``{video_id}`` tag.
* embed template: string template used to build the new embed code. Needs the
  ``{video_link}`` tag.
* validation template: string template used to build the link used to validate
  that the video is still available. This is the link to the video itself (as
  seen on the provider's website). Needs the ``{video_id}`` tag.
* matches: regular expressions used to "match" a video embed code to a video
  provider. Must capture the video id.

.. _format: http://docs.python.org/library/functions.html#format
