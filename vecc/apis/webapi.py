#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


class APIError(Exception):
    """Return API's specific errors if needed"""
    # TODO Define some error codes ?
    # 3xx and 4xx and 5xx are source (HTTP) related

    def __init__(self, *args):
        if isinstance(args, tuple) and len(args) > 1:
            self.errno = args[0]
            self.msg = " ".join(args[1:])
            if self.errno >= 300:
                errtxt = "HTTP Errno"
            else:
                errtxt = "Errno"
            super(APIError, self).__init__(
                "[{} {}] {}".format(errtxt, self.errno, self.msg))
        else:
            super(APIError, self).__init__("".join(args))


class WebAPI(object):
    def check(self, video_id):
        """Check if the video exists.

        :params video_id: the video ID (its format is specific to the service)

        :return bool: True if the video is found false otherwise.
        """
        raise NotImplementedError('This method must be inherited by the children')

    @property
    def video_data(self):
        """Return got informations from the checked video.

        :return dict: wanted infos as following:
        >>> {
        >>>     'title': 'Video title',
        >>>     'description': 'Video description',
        >>>     'image': 'Image associated with the video',
        >>>     'duration': 'Video duration as %H:%M:%S',
        >>>     'status': 'True if the video is public and operational, else False'
        >>> }
        """
        # NOTE: get the image with the higher quality if possible
        raise NotImplementedError('This method must be inherited by the children')


def convertduration(original):
    #convert duration in secs to H:M:S
    m, s = divmod(int(original), 60)
    h, m = divmod(m, 60)

    return "%d:%02d:%02d" % (h, m, s)

