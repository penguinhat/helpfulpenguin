"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from redirects.models import LiveRedirect, HALF_DAY, FOUR_WEEKS, DURATION_CHOICES
from redirects.utils import get_unused_slug, VALID_WORDS


class RedirectCreationTest(TestCase):

    def test_live_redirect_creation(self):

        default_kwargs = {
            'url':'http://www.example.com',
            'duration':HALF_DAY
        }

        r = LiveRedirect(**default_kwargs)

        r.save()

        for duration,_ in DURATION_CHOICES:
            kwargs = default_kwargs
            kwargs['duration'] = duration

            r = LiveRedirect(**kwargs)

            r.save()


    def test_slug_generation(self):
        """
        Tests that slugs of all possible lengths can be generated without causing
        an Exception
        """

        for i in xrange(1,len(VALID_WORDS)):

            get_unused_slug(i)

    def test_100_redirects_creation(self):

        count = 0

        default_kwargs = {
            'url':'http://www.example.com',
            'duration':FOUR_WEEKS
        }

        while count < 100:
            r = LiveRedirect(**default_kwargs)
            r.save()
            count += 1