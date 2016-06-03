#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core functions.

All needed functions to match a video, get its new embed code, validate it...

"""

import re

import requests

from .providers import PROVIDERS


def match(embed_code, providers=PROVIDERS):
    """Return (video_id, provider) by looking for a match on the embed code."""
    for provider, data in providers.items():
        for match in data['matches']:
            res = re.search(match, embed_code,
                            flags=re.IGNORECASE | re.MULTILINE)
            if res:  # matches video_id in res.groups()[0]
                return res.groups()[0], provider
    return None, None


def get_link(video_id, provider, providers=PROVIDERS):
    """Return the full video link from a video id and a provider."""
    if provider not in providers:
        return None
    data = providers[provider]
    template = data['link_template']
    return template.format(video_id=video_id)


def get_validation(video_id, provider, providers=PROVIDERS):
    """Return the video validation link from a video id and a provider."""
    if provider not in providers:
        return None
    data = providers[provider]
    template = data['validation_template']
    return template.format(video_id=video_id)


def get_clean_code(video_id, provider, providers=PROVIDERS):
    """Return the new embed code from a video id and a provider."""
    if provider not in providers:
        return None
    data = providers[provider]
    video_link = get_link(video_id, provider, providers)
    template = data['embed_template']
    return template.format(video_link=video_link)


def validate(video_id, provider, timeout=10, providers=PROVIDERS,
             helper=requests):
    """True if the status code of the url is less than 400."""
    validation_link = get_validation(video_id, provider, providers)
    if validation_link is None:
        return
    try:
        req = helper.head(validation_link, timeout=timeout)
        return req.status_code < 400
    except requests.exceptions.Timeout:
        raise
    except:
        return False

