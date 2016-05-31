#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import sys
import urllib
import requests

from . import __version__
from .core import get_clean_code, match, validate

from apis.webapi import APIError
from apis.youtube import YoutubeAPI
from apis.dailymotion import DailymotionAPI
from apis.vimeo import VimeoAPI
from apis.facebook import FacebookAPI


PROVIDERS_API = {
    'youtube': YoutubeAPI,
    'dailymotion': DailymotionAPI,
    'vimeo': VimeoAPI,
    'facebook': FacebookAPI,
}


def clean(args):
    """Clean the embed code, and optionally validate it."""
    video_id, provider = match(args.code)
    clean_code = get_clean_code(video_id, provider)
    if clean_code:
        print("video id:", video_id)
        print("provider:", provider)
        print("embed code:", clean_code)
        if args.validate:
            setattr(args, 'video_id', video_id)
            setattr(args, 'provider', provider)
            valid(args)
        sys.exit()
    print("Provider not found")
    sys.exit(1)


def valid(args):
    """Validate that a video is still available."""
    try:
        valid = validate(args.video_id, args.provider, args.timeout)
    except requests.exceptions.Timeout:
        print("Timeout while validating the video")
        sys.exit(4)  # Correspond to a server timeout

    if valid is None:
        print("Provider not found")
        sys.exit(1)
    elif valid:
        print("This video is still available")
        sys.exit()
    else:
        print("This video is not available anymore")
        sys.exit(2)


def extract(code, extensions = ['mp4']):
    video_id, provider = match(code)
    clean_code = get_clean_code(video_id, provider)
    real_link = get_link(video_id, provider)
    if not clean_code:
        extension = code[-4:].lower()
        for ext in extensions:
            if extension == "." + ext:
                #test if url exists
                vidinfos = {
                    'provider': ext,
                    'real_link': code,
                }
                try:
                    if code[0:2] == '//':
                        getcode = 'http:'+code
                    else:
                        getcode = code
                    codeid = urllib.urlopen(getcode).getcode()
                    if codeid == 200:
                        vidinfos['status'] = True
                    else:
                        vidinfos["errno"] = codeid
                        if 300 <= codeid < 400:
                            vidinfos["errmsg"] = 'HTTP Redirection'
                        if 400 <= codeid < 500:
                            vidinfos["errmsg"] = 'HTTP Client Error'
                        if 500 <= codeid < 600:
                            vidinfos["errmsg"] = 'HTTP Server Error'
                        vidinfos['status'] = False
                except IOError as e:
                    vidinfos['status'] = False
                    vidinfos["errno"] = -1
                    vidinfos["errmsg"] = e.strerror
                return vidinfos
        return {
            'status': False,
            'errno' : -2
            }
    ret = {
        'video_id': video_id,
        'provider': provider,
        'clean_code': clean_code,
        'real_link': real_link}
    try:
        Api = PROVIDERS_API[provider]
    except KeyError:
        sys.exit()
    api = Api()
    try:
        if api.check(video_id):
            details = api.video_data
            ret.update(details)
        else:
            ret["status"] = False
    except APIError as err:
        ret["errno"] = err.errno
        ret["errmsg"] = err.msg
        ret["status"] = False
    except Exception as e:
        if hasattr(e, '__module__') and e.__module__ == "requests.exceptions":
            ret["errno"] = -1
            ret["errmsg"] = "Error type: " + e.__class__.__name__
        ret["status"] = False
    return ret


def main():
    parser = argparse.ArgumentParser(description='Video Embed Code Cleaner.')
    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=10,
        help='timeout for the validation (10 seconds by default)')
    subparsers = parser.add_subparsers(title='sub-commands')

    parser_clean = subparsers.add_parser('clean', help='clean the embed code')
    parser_clean.add_argument('code', help='video embed code to clean')
    parser_clean.add_argument(
        '-v', '--validate', action='store_true',
        help='also validate that the video is still available')
    parser_clean.set_defaults(func=clean)

    parser_validate = subparsers.add_parser(
        'validate', help='validate that the video is still available')
    parser_validate.add_argument('video_id', help='id of the video')
    parser_validate.add_argument('provider', help='provider of the video')
    parser_validate.set_defaults(func=valid)

    parser_extract = subparsers.add_parser(
        'extract', help='Extract informations from the video')
    parser_extract.add_argument('code',
        help='video embed code from which extract infos')
    parser_extract.set_defaults(func=extract)

    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {0}'.format(__version__))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
