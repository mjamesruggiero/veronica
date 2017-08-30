import xml.etree.ElementTree as ElementTree

from base import BaseTestCase
from flask import url_for

class ViewsTests(BaseTestCase):
    def test_index_should_render_default_view(self):
        self.client.get('/')
        self.assert_template_used('index.html')

    def test_post_to_welcome_should_serve_twiml(self):
        response = self.client.post('/veronica/welcome')
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Gather/Play") is None
        assert twiml.findall("./Gather")[0].attrib["action"] == url_for('menu')
