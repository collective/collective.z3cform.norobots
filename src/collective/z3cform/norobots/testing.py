from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from collective.z3cform.norobots.tests.utils import PLONE_VERSION

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    # BBB for Plone 5.0 and lower.
    get_installer = None

class NorobotsSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML, install the products and call its initialize() function
        # Load ZCML for this package
        import collective.z3cform.norobots
        self.loadZCML(package=collective.z3cform.norobots)
        z2.installProduct(app, 'collective.z3cform.norobots')

    def setUpPloneSite(self, portal):
        # Configure the products using the Quick Installer tool
        if get_installer is None:
            qi = portal['portal_quickinstaller']
        else:
            qi = get_installer(portal)
        qi.installProducts( ('collective.z3cform.norobots',) )

    def tearDownZope(self, app):
        # Uninstall products
        z2.uninstallProduct(app, 'collective.z3cform.norobots')

    def tearDownPloneSite(self, portal):
        # Unconfigure the products using the Quick Installer tool
        if get_installer is None:
            qi = portal['portal_quickinstaller']
        else:
            qi = get_installer(portal)
        qi.uninstallProducts( ('collective.z3cform.norobots',) )

NOROBOTS_FIXTURE = NorobotsSandboxLayer()
NOROBOTS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NOROBOTS_FIXTURE, ),
                       name="collective.z3cform.norobots:Integration")
NOROBOTS_FUNCTIONNAL_TESTING = \
    FunctionalTesting(bases=(NOROBOTS_FIXTURE, ),
                      name="collective.z3cform.norobots:Integration")