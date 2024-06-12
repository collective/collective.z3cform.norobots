from collective.z3cform.norobots.testing import NOROBOTS_FUNCTIONNAL_TESTING
from collective.z3cform.norobots.testing import NOROBOTS_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.testing.zope import Browser

import transaction
import unittest


class TestIntegrationSamplePackage(unittest.TestCase):
    layer = NOROBOTS_INTEGRATION_TESTING

    def test_constraints_isValidEmail(self):
        from collective.z3cform.norobots.plone_forms.constraints import isEmail

        self.assertTrue(isEmail("john.doe@plone.org"))

    def test_constraints_isNotValidEmail(self):
        from collective.z3cform.norobots.plone_forms.constraints import isEmail
        from collective.z3cform.norobots.plone_forms.constraints import IsEmailError

        with self.assertRaises(IsEmailError):
            isEmail("i'm not a  valid email")


class TestFunctionalSamplePackage(unittest.TestCase):

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

    def test_sample_package(self):
        from io import StringIO
        from lxml import etree

        browser = self._manager_browser()
        browser.open(f"{self.portal.absolute_url()}/z3cform-contact-info")
        tree = etree.parse(StringIO(browser.contents), etree.HTMLParser())

        result = tree.xpath("//form[@id='z3cform_contact_info_form']")
        self.assertEqual(1, len(result), "the sample form is not present")

        result = tree.xpath("//input[@name='form.widgets.fullname']")
        self.assertEqual(1, len(result), "fullname widget is not present")

        result = tree.xpath("//input[@name='form.widgets.email']")
        self.assertEqual(1, len(result), "email widget is not present")

        result = tree.xpath("//input[@name='form.widgets.subject']")
        self.assertEqual(1, len(result), "subject widget is not present")

        result = tree.xpath("//textarea[@name='form.widgets.message']")
        self.assertEqual(1, len(result), "message widget is not present")

        result = tree.xpath("//input[@name='form.widgets.norobots']")
        self.assertEqual(1, len(result), "norobots widget is not present")

        # send the form
        browser.getControl("Send").click()
        self.assertIn(
            "Please correct the indicated errors and don't forget to fill in the field 'Are you a human ?'.",
            browser.contents,
            "the error message is missing!",
        )


class TestFunctionalMacroView(unittest.TestCase):

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

    def test_sample_package(self):
        from io import StringIO
        from lxml import etree

        browser = self._manager_browser()
        browser.open(f"{self.portal.absolute_url()}/simple-form-with-macro-view")
        tree = etree.parse(StringIO(browser.contents), etree.HTMLParser())

        result = tree.xpath("//input[@name='form.widgets.fullname']")
        self.assertEqual(1, len(result), "fullname widget is not present")

        result = tree.xpath("//input[@name='norobots']")
        self.assertEqual(1, len(result), "norobots widget is not present")
