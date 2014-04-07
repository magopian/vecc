#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from .core import match, get_link, get_validation, get_clean_code, validate

PROVIDERS = {
    'Foo': {
        'link_template': r"""http://{video_id}""",
        'embed_template': r"""some code {video_link}""",
        'validation_template': r"""http://httpbin.org/status/{video_id}""",
        'matches': [r"""foo_video/(.*)""", r"""foo_video_embed/(.*)"""]
    },
    'Bar': {
        'link_template': r"""http://{video_id}""",
        'embed_template': r"""some code {video_link}""",
        'validation_template': r"""http://httpbin.org/status/{video_id}""",
        'matches': [r"""bar_video/(.*)""", r"""bar_video_embed/(.*)"""]
    },
}


class Helper(object):
    """Mock the requests.head calls."""

    def __init__(self, status_code):
        self.status_code = status_code

    def head(self, link, timeout):
        if self.status_code is None:
            raise
        return self


class CoreTest(TestCase):

    def test_match_video(self):
        video_id, provider = match('stuff foo_video/barbaz', PROVIDERS)
        self.assertEqual(video_id, 'barbaz')
        self.assertEqual(provider, 'Foo')

    def test_match_video_other_match_same_provider(self):
        video_id, provider = match('stuff foo_video_embed/barbaz', PROVIDERS)
        self.assertEqual(video_id, 'barbaz')
        self.assertEqual(provider, 'Foo')

    def test_match_video_other_provider(self):
        video_id, provider = match('stuff bar_video_embed/barbaz', PROVIDERS)
        self.assertEqual(video_id, 'barbaz')
        self.assertEqual(provider, 'Bar')

    def test_match_video_ignore_case(self):
        video_id, provider = match('STUFF FOO_VIdeo/barbaz', PROVIDERS)
        self.assertEqual(video_id, 'barbaz')
        self.assertEqual(provider, 'Foo')

    def test_match_video_multiline(self):
        video_id, provider = match('stuff\nfoo_video/barbaz', PROVIDERS)
        self.assertEqual(video_id, 'barbaz')
        self.assertEqual(provider, 'Foo')

    def test_match_provider_not_found(self):
        video_id, provider = match('stuff video/barbaz', PROVIDERS)
        self.assertTrue(video_id is None)
        self.assertTrue(provider is None)

    def test_get_link(self):
        link = get_link('barbaz', 'Foo', PROVIDERS)
        self.assertEqual(link, 'http://barbaz')

    def test_get_link_provider_not_found(self):
        link = get_link('barbaz', 'Baz', PROVIDERS)
        self.assertTrue(link is None)

    def test_get_validation(self):
        validation = get_validation('barbaz', 'Foo', PROVIDERS)
        self.assertEqual(validation, 'http://httpbin.org/status/barbaz')

    def test_get_validation_provider_not_found(self):
        validation = get_link('barbaz', 'Baz', PROVIDERS)
        self.assertTrue(validation is None)

    def test_get_clean_code(self):
        clean_code = get_clean_code('barbaz', 'Foo', PROVIDERS)
        self.assertEqual(clean_code, 'some code http://barbaz')

    def test_get_clean_code_provider_not_found(self):
        clean_code = get_clean_code('barbaz', 'Baz', PROVIDERS)
        self.assertTrue(clean_code is None)

    def test_validate_200(self):
        validated = validate('barbaz', 'Foo', 10, PROVIDERS, Helper(200))
        self.assertTrue(validated)

    def test_validate_301(self):
        validated = validate('barbaz', 'Foo', 10, PROVIDERS, Helper(301))
        self.assertTrue(validated)

    def test_validate_400(self):
        validated = validate('barbaz', 'Foo', 10, PROVIDERS, Helper(400))
        self.assertFalse(validated)

    def test_validate_provider_not_found(self):
        validated = validate('barbaz', 'Baz', 10, PROVIDERS, Helper(200))
        self.assertFalse(validated)

    def test_validate_raise(self):
        validated = validate('barbaz', 'Foo', 10, PROVIDERS, Helper(None))
        self.assertFalse(validated)
