#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import requests
import re
import facepy
import dateutil.parser
from facepy.exceptions import FacebookError

from .webapi import WebAPI, APIError, convertduration


def set_fb_token(token):
    FacebookAPI.__token__ = token


class FacebookAPI(WebAPI):
    __token__ = 'not_set_put_one'
    __part__ = ('created_time,description,length,picture,source,' +
        'title,status,published,privacy,content_tags,content_category')
    __url__ = ('/v2.6/{video_id}?fields={part}')

    def __init__(self):
        self._data = {}
        self._results = None
        self._video_id = 0

    def _call_api(self):
        fb = facepy.GraphAPI(self.__token__)
        built_url = self.__url__.format(
            video_id=self._video_id,
            part=self.__part__)
        try:
            answer = fb.get(built_url)
        except FacebookError as fber:
            raise APIError(fber.code, fber.message)
        except:
            raise APIError(500, "Facebook API Error")
        else:
            if "status" in answer:
                self._data = answer
                return True
            else:
                raise APIError(404, 'Facebook video is not available')

    def _is_ok(self):
        """Extract privacy policy and upload status to determine availability."""
        if (self._data['status']['video_status'] == 'ready' and
                self._data['published'] and
                self._data['privacy']['value'] == 'EVERYONE'):
            return True
        return False

    def check(self, video_id):
        if video_id != self._video_id:
            self._results = None
        self._video_id = video_id
        return self._call_api()

    @property
    def video_data(self):
        if not self._data:
            return {}
        if not self._results:
            self._results = {
                'title': self._data.get('title', ''),
                'description': self._data.get('description', ''),
                'duration': convertduration(self._data.get('length', '0')),
                'status': self._is_ok()
            }
            if 'picture' in self._data:
                self._results['image'] = self._data['picture']
            if 'created_time' in self._data:
                self._results['created_date'] = \
                    dateutil.parser.parse(self._data['created_time'])
            if 'content_tags' in self._data:
                self._results['tags'] = self._data['content_tags']
        return self._results
