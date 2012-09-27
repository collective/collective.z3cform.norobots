import string
import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from zope.component import getUtility

from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings
from plone.registry.interfaces import IRegistry

from collective.z3cform.norobots.testing import NOROBOTS_INTEGRATION_TESTING


class TestInstall(unittest.TestCase):

    layer = NOROBOTS_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product 
            installed
        """
        portal_quickinstaller = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(portal_quickinstaller.isProductInstalled('collective.z3cform.norobots'),
                        'package appears not to have been installed')

    def test_registry(self):
        registry = getUtility(IRegistry)
        
        # Check 'question' entry is in the registry
        self.assertTrue(registry.get('collective.z3cform.norobots.browser.interfaces.INorobotsWidgetSettings.questions', None is not None),
                         'record in the registry appears to be not properly installed')

    def test_control_panel_is_installed(self):
        portal_controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        configlets = [ai['id'] for ai in portal_controlpanel.listActionInfos(check_permissions=0)]
        self.assertTrue('collective.z3cform.norobots.settings' in configlets)

class TestUninstall(unittest.TestCase):

    layer = NOROBOTS_INTEGRATION_TESTING
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        
        # Remove the product using the Quick Installer tool
        portal_quickinstaller = getToolByName(self.portal, 'portal_quickinstaller')
        portal_quickinstaller.uninstallProducts( ('collective.z3cform.norobots',) )
        
    def test_product_is_not_installed(self):
        """ Validate that our products is not yet installed
        """
        portal_quickinstaller = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertFalse(portal_quickinstaller.isProductInstalled('collective.z3cform.norobots'),
                        'package appears to be already installed')

    def test_registry(self):
        registry = getUtility(IRegistry)
        norobots_settings = registry.forInterface(INorobotsWidgetSettings)
        
        # Check 'question' entry is again in the registry, 
        # i.e. not removed when the module is uninstalled
        self.assertTrue(registry.get('collective.z3cform.norobots.browser.interfaces.INorobotsWidgetSettings.questions', None is not None),
                         'record in the registry must be kept when the module is uninstalled')

    def test_control_panel_is_not_installed(self):
        portal_controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        configlets = [ai['id'] for ai in portal_controlpanel.listActionInfos(check_permissions=0)]
        self.assertFalse('collective.z3cform.norobots.settings' in configlets)
    