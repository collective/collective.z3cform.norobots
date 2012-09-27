from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from Products.CMFCore.utils import getToolByName

from collective.z3cform.norobots.tests.utils import PLONE_VERSION

class NorobotsSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML, install the products and call its initialize() function 
        
        if PLONE_VERSION == 4.0:
            # plone.app.registry is not include in Plone 4.0 core
            import plone.app.registry
            self.loadZCML(package=plone.app.registry)
            z2.installProduct(app, 'plone.app.registry')
        
        # Load ZCML for this package
        import collective.z3cform.norobots
        self.loadZCML(package=collective.z3cform.norobots)
        z2.installProduct(app, 'collective.z3cform.norobots')

    def setUpPloneSite(self, portal):
        # Configure the products using the Quick Installer tool 
        portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
        
        if PLONE_VERSION == 4.0:
            # plone.app.registry is not include in Plone 4.0 core
            portal_quickinstaller.installProducts( ('plone.app.registry',) )
        
        portal_quickinstaller.installProducts( ('collective.z3cform.norobots',) )

    def tearDownZope(self, app):
        # Uninstall products
        
        z2.uninstallProduct(app, 'collective.z3cform.norobots')
        
        if PLONE_VERSION == 4.0:
            # plone.app.registry is not include in Plone 4.0 core
            z2.uninstallProduct(app, 'plone.app.registry')

    def tearDownPloneSite(self, portal):
        # Unconfigure the products using the Quick Installer tool
        portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
        
        portal_quickinstaller.uninstallProducts( ('collective.z3cform.norobots',) )
        
        if PLONE_VERSION == 4.0:
            # plone.app.registry is not include in Plone 4.0 core        
            portal_quickinstaller.uninstallProducts( ('plone.app.registry',) )

NOROBOTS_FIXTURE = NorobotsSandboxLayer()
NOROBOTS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NOROBOTS_FIXTURE, ),
                       name="collective.z3cform.norobots:Integration")
NOROBOTS_FUNCTIONNAL_TESTING = \
    FunctionalTesting(bases=(NOROBOTS_FIXTURE, ),
                      name="collective.z3cform.norobots:Integration")