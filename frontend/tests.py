from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from redirects.models import LiveRedirect, HALF_DAY

class FrontendTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()

    def test_can_create_redirect(self):
        """
        Unittest to ensure that all the frontend pages load correctly
        """

        #Homepage
        self.browser.get(self.live_server_url)

        #Look for the submit button and the two inputs
        url_field = self.browser.find_element_by_id('id_url')
        duration_field = self.browser.find_element_by_id('id_duration')

        # Enter something into the inputs
        url_field.send_keys('www.example.com')
        duration_field.send_keys(Keys.DOWN)

        submit_button = self.browser.find_element_by_tag_name('input')
        submit_button.submit()

    def test_can_be_redirected(self):
        """
        Unittest to ensure that all the frontend pages load correctly
        """

        url = 'http://www.example.com'

        r = LiveRedirect(url=url,duration=HALF_DAY)
        r.save()

        TEST_URLS = [
            '%s/%s' % (self.live_server_url,r.slug),
            '%s/%s/' % (self.live_server_url,r.slug),
        ]

        for url in TEST_URLS:

            self.browser.get(url)

            body = self.browser.find_element_by_tag_name('body')

            # Check that it is not a 404 or 500
            self.assertNotIn('404',body.text)
            self.assertNotIn('500',body.text)

            # Slug page should always state what the url is
            self.assertIn(r.url, body.text, 'Link url not displayed on slug page!')

            # Slug page should always have a link to the correct page!
            links = self.browser.find_elements_by_tag_name('a')

            ok = False
            for link in links:
                if link.get_attribute('href').rstrip('/') == r.url.rstrip('/'):
                    ok = True
                    break

            self.failIf(not ok,'No link to target!')

    def test_pages_are_valid(self):
        """
        Check that a page is valid. A valid page has a title, is not
        a 404 or 500 page and correctly inheirts from base
        """

        url = 'http://www.example.com'

        r = LiveRedirect(url=url,duration=HALF_DAY)
        r.save()

        TEST_URLS = [
            '%s/' % self.live_server_url,
            '%s/%s' % (self.live_server_url,r.slug),
            '%s/%s/' % (self.live_server_url,r.slug),
        ]

        for url in TEST_URLS:
            self.browser.get(url)

            body = self.browser.find_element_by_tag_name('body')
            title = self.browser.find_element_by_tag_name('title')

            # Check that it is not a 404 or 500
            self.assertNotIn('404',body.text,"%s returns 404!" % url)
            self.assertNotIn('500',body.text,"%s returns 500!" % url)

            # Check that title is valid

            self.assertNotIn('NO-TITLE',title.text,"%s is using default base title!" % url)
            self.assertIsNotNone(title.text, "%s has no title!" % url)
            self.assertNotEquals('',title.text, "%s has no title!" % url)

    def test_can_access_admin(self):
        """
        Unittest to ensure that all the frontend pages load correctly
        """

        #Homepage
        self.browser.get(self.live_server_url + '/admin/')

        body = self.browser.find_element_by_tag_name('body')

        self.assertIn('Django administration',body.text,"Cannot get to /admin/")