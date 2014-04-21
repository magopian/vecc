#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import sys

import requests

from . import __version__
from .core import get_clean_code, match, validate


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
    sys.exit(2)


def valid(args):
    """Validate that a video is still available."""
    try:
        valid = validate(args.video_id, args.provider, args.timeout)
    except requests.exceptions.Timeout:
        print("Timeout while validating the video")
        sys.exit(1)

    if valid is None:
        print("Provider not found")
        sys.exit(2)
    elif valid:
        print("This video is still available")
        sys.exit()
    else:
        print("This video is not available anymore")
        sys.exit(3)


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

    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {0}'.format(__version__))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
