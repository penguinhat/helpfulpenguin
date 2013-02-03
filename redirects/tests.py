from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

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

    def test_api(self):

        client = Client()

        # POST a new redirect
        new_redirect_data = {
            'duration':HALF_DAY,
            'url':'http://www.example.com'
        }

        post_response = client.post(reverse('live_redirect_api'),new_redirect_data)

        # Get the slug back and check that we can find our new LiveRedirect
        slug = post_response.data['slug']

        get_response = client.get(
            reverse('live_redirect_details',kwargs={'slug':slug}))

        self.assertEqual(post_response.data['slug'],get_response.data['slug'])
        self.assertEqual(post_response.data['created'],get_response.data['created'])
        self.assertEqual(post_response.data['duration'],get_response.data['duration'])
        self.assertEqual(post_response.data['url'],get_response.data['url'])
