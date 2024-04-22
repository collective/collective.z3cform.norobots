from collective.z3cform.norobots.testing import NOROBOTS_FUNCTIONNAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import Browser

import transaction
import unittest


class TestFunctionalControlpanel(unittest.TestCase):

    layer = NOROBOTS_FUNCTIONNAL_TESTING

    def _manager_browser(self):
        transaction.commit()
        # Set up browser
        browser = Browser(self.layer["app"])
        browser.handleErrors = False
        browser.addHeader(
            "Authorization",
            "Basic {}:{}".format(
                SITE_OWNER_NAME,
                SITE_OWNER_PASSWORD,
            ),
        )
        return browser

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_controlpanel_textarea(self):
        from io import StringIO
        from lxml import etree

        browser = self._manager_browser()
        browser.open(f"{self.portal.absolute_url()}/@@norobots-controlpanel")
        tree = etree.parse(StringIO(browser.contents), etree.HTMLParser())

        result = tree.xpath("//textarea[@id='form-widgets-questions']/@rows")
        self.assertEqual("15", result[0], "The textarea should be have 15 lines")


5
