#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import requests
import re
import datetime

from .webapi import WebAPI, APIError, convertduration


class DailymotionAPI(WebAPI):
    __fields__ = ('fields=created_time,description,duration,id,status,'
        'thumbnail_url,title,')
    __url__ = "https://api.dailymotion.com/video/{video_id}/?{fields}"

    def __init__(self):
        self._data = {}
        self._results = None
        self._pattern = re.compile(
            r"""P([0-9]{1,2}D)?(T)?([0-9]{1,2}H)?([0-9]{1,2}M)?([0-9]{1,2}S)?"""
        )
        self._video_id = 0

    def _call_api(self):
        built_url = self.__url__.format(
            video_id=self._video_id,
            fields=self.__fields__)

        answer = requests.get(built_url)
        self._data = json.loads(answer.content)
        errorstr = ""
        if answer.status_code < 300:
            if 'status' in self._data:
                return True
        else:
            err = self._data.get('error', None)
            if err:
                errorstr = err.get('message','')

        # Manage error situations
        error_msg = 'Unbound Source Error'
        if 300 <= answer.status_code < 400:
            error_msg = 'HTTP Redirection'
        if 400 <= answer.status_code < 500:
            error_msg = 'HTTP Client Error'
        if 500 <= answer.status_code < 600:
            error_msg = 'HTTP Server Error'
        if errorstr:
            error_msg += ": "+errorstr
        raise APIError(answer.status_code, error_msg)

    def _is_ok(self, status):
        """Extract privacy policy and upload status to determine availability."""
        if status == "published":
            return True
        return False

    def check(self, viedo_id):
        if viedo_id != self._video_id:
            self._results = None
        self._video_id = viedo_id
        return self._call_api()

    @property
    def video_data(self):
        if not self._data:
            return {}
        if not self._results:
            our_video = self._data
            self._results = {
                'title': our_video['title'],
                'description': our_video['description'] if our_video['description'] else "",
                'image': our_video['thumbnail_url'],
                'duration': convertduration(
                    our_video['duration']),
                'status': self._is_ok(our_video['status']),
                'created_date': datetime.datetime.fromtimestamp(our_video['created_time'])
            }
        return self._results
