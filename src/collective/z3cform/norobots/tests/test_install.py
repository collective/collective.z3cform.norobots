# -*- coding: utf-8 -*-
from collective.z3cform.norobots.testing import NOROBOTS_INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    # BBB for Plone 5.0 and lower.
    get_installer = None

PROJECTNAME = "collective.z3cform.norobots"


class TestInstall(unittest.TestCase):

    layer = NOROBOTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_is_installed(self):
        """Test if collective.z3cform.norobots is installed."""
        self.assertTrue(
            self.installer.is_product_installed(
                "collective.z3cform.norobots",
            )
        )

    def test_registry(self):
        registry = getUtility(IRegistry)
        # Check 'question' entry is in the registry
        self.assertTrue(
            registry.get(
                "collective.z3cform.norobots.browser.interfaces.INorobotsWidgetSettings.questions",
                False,
            ),
            "record in the registry appears to be not properly installed",
        )

    def test_control_panel_is_installed(self):
        portal_controlpanel = getToolByName(self.portal, "portal_controlpanel")
        actions = [i.id for i in portal_controlpanel.listActions()]
        self.assertTrue("collective.z3cform.norobots.settings" in actions)


class TestUninstall(unittest.TestCase):

    layer = NOROBOTS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        if get_installer:
            self.installer = get_installer(self.portal, self.request)
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        self.installer.uninstall_product("collective.z3cform.norobots")

    def test_product_is_not_installed(self):
        """Validate that our products is not yet installed"""
        self.assertFalse(
            self.installer.is_product_installed("collective.z3cform.norobots"),
        )

    def test_registry(self):
        registry = getUtility(IRegistry)
        self.assertNotIn(
            "collective.z3cform.norobots.browser.interfaces.INorobotsWidgetSettings.questions",
            registry,
        )

    def test_control_panel_is_not_installed(self):
        portal_controlpanel = api.portal.get_tool("portal_controlpanel")
        actions = [i.id for i in portal_controlpanel.listActions()]
        self.assertFalse("collective.z3cform.norobots.settings" in actions)
