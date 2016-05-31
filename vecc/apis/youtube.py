#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import requests
import re
import dateutil.parser

from .webapi import WebAPI, APIError


class YoutubeAPI(WebAPI):
    __key__ = 'AIzaSyC9A_hUq6r2IMgoMVU15CL4OFRoeTzY9vU'
    __part__ = 'snippet,contentDetails,status'
    __url__ = ('https://www.googleapis.com/youtube/v3/videos?id={video_id}'
            '&part={part}&key={key}')

    def __init__(self):
        self._data = {}
        self._results = None
        self._pattern = re.compile(
            r"""P(?P<D>[0-9]{1,2}D)?(T)?(?P<H>[0-9]{1,2}H)?(?P<M>[0-9]{1,2}M)?(?P<S>[0-9]{1,2}S)?"""
        )
        self._video_id = 0

    def _call_api(self):
        built_url = self.__url__.format(
            video_id=self._video_id,
            part=self.__part__,
            key=self.__key__)
        answer = requests.get(built_url)
        if answer.status_code < 300:
            self._data = json.loads(answer.content)
            if self._data['pageInfo']['totalResults'] == 1:
                return True
            else:
                raise APIError(404, 'Youtube video is not available')

        # Manage error situations
        error_msg = 'Unbound Source Error'
        if 300 <= answer.status_code < 400:
            error_msg = 'HTTP Redirection'
        if 400 <= answer.status_code < 500:
            error_msg = 'HTTP Client Error'
        if 500 <= answer.status_code < 600:
            error_msg = 'HTTP Server Error'
        raise APIError(answer.status_code, error_msg)

    def _parse_duration(self, yduration):
        """Convert Youtube duration (ISO 8601 format) to %H:%M:%S duration."""
        ma = self._pattern.match(yduration)
        dic = ma.groupdict()
        for k in dic:
            if dic[k]:
                dic[k] = int(dic[k][:-1])
            else:
                dic[k] = 0
        if dic['D'] > 0:
            dic['H'] += dic['D'] * 24
        return '%(H)02d:%(M)02d:%(S)02d' % dic

    def _is_ok(self, status):
        """Extract privacy policy and upload status to determine availability."""
        if status['uploadStatus'] in ('processed', 'uploaded') \
                and status['privacyStatus'] != 'private':
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
            our_video = self._data['items'][0]
            desc = our_video['snippet']['description']
            self._results = {
                'title': our_video['snippet']['title'],
                'description': desc if desc else "",
                'image': our_video['snippet']['thumbnails']['high']['url'],
                'duration': self._parse_duration(
                    our_video['contentDetails']['duration']),
                'status': self._is_ok(our_video['status']),
                'created_date': dateutil.parser.parse(our_video['snippet']['publishedAt'])
            }
        return self._results
