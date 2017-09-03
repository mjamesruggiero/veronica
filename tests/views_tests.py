import xml.etree.ElementTree as ElementTree

from base import BaseTestCase
from flask import url_for
import sys
import logging

logging.basicConfig(
    format="%(levelname)-10s %(asctime)s %(filename)s %(lineno)d %(message)s",
    level=logging.ERROR
)
log = logging.getLogger(sys.argv[0])

class ViewsTests(BaseTestCase):
    def test_index_should_render_default_view(self):
        """views - index renders default view"""
        self.client.get('/')
        self.assert_template_used('index.html')

    def test_post_to_welcome_should_serve_twiml(self):
        """views - posting to welcome serves twiml"""
        response = self.client.post('/veronica/welcome')
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Gather/Play") is None
        assert twiml.findall("./Gather")[0].attrib["action"] == url_for('menu')


    def test_post_to_with_digit_1_serves_twiml_say_once_and_hangup(self):
        """views - posting with 1 serves Twiml, say 2 times and hang up"""
        response = self.client.post('/veronica/menu',
                                    data=dict(Digits='1'),
                                    follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        logging.debug("twiml is {}".format(response.data))
        assert len(twiml.findall("./Say")) == 1
        assert not twiml.findall("./Hangup") is None

    def test_post_to_menu_with_digit_other_than_1_or_2_redirects_to_welcome(self):
        """views - post to menu with non-recognized digit redirects to welcome"""
        response = self.client.post('/veronica/menu',
                                    data=dict(Digits=9),
                                    follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Redirect") is None
        assert twiml.findall("./Redirect")[0].text == url_for('welcome')
