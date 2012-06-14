from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class NorobotsSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.z3cform.norobots
        xmlconfig.file('configure.zcml',
                       collective.z3cform.norobots,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.z3cform.norobots:default')

NOROBOTS_FIXTURE = NorobotsSandboxLayer()
NOROBOTS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NOROBOTS_FIXTURE, ),
                       name="collective.z3cform.norobots:Integration")