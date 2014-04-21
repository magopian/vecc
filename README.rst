########################
Video Embed Code Cleaner
########################

.. image:: https://secure.travis-ci.org/magopian/vecc.png
   :alt: Build Status
   :target: https://travis-ci.org/magopian/vecc

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
      -t TIMEOUT, --timeout TIMEOUT
                        timeout for the validation (10 seconds by default)
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


Return codes
============

There's three different return codes possible:

* ``1``: Timeout while validating (doing a ``HEAD`` request) the video
* ``2``: Provider not found
* ``3``: The video is not available anymore


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


Changelog
=========

* **v0.12**:

  * Fix previous commit that broke ``vecc.clean``

* **v0.11**:

  * added a ``timeout`` parameter for the validation
  * now uses proper return codes for failures

* **v0.10**:

  * fix print in py2 following porting to py3

* **v0.9**:

  * use schema-less urls for the default providers
  * make travis use tox
  * provide a wheel package

* **v0.8**:

  * compatible python 2.6 to python 3.3
  * 100% test coverage

* **v0.7**:

  * dropped allowfullscreen
  * added autoPlay=1&related=0 on video links

* **v0.6**:

  * video size of the cleaned embed code is now 480x395
  * all embed codes with iframes use the same format with
    allowfullscreen="true", autoPlay="1", related="0"

* **v0.5**:

  * compatibility with python2.6: ``argparse`` as a dependency

* **v0.4**:

  * compatibility with python2.6: ``format`` needs field numbers
