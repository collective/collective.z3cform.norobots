from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

from collective.z3cform.norobots.tests.utils import PLONE_VERSION

class NorobotsSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):

        if PLONE_VERSION == 4.0:
            # plone.app.registry is not include in Plone 4.0 core
            # Load ZCML for plone.app.registry
            import plone.app.registry
            xmlconfig.file('configure.zcml',
                           plone.app.registry,
                           context=configurationContext)
        
        # Load ZCML for this package
        import collective.z3cform.norobots
        xmlconfig.file('configure.zcml',
                       collective.z3cform.norobots,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        
        if PLONE_VERSION == 4.0:
            # plone.app.registry is not include in Plone 4.0 core
            applyProfile(portal, 'plone.app.registry:default')
        
        applyProfile(portal, 'collective.z3cform.norobots:default')

NOROBOTS_FIXTURE = NorobotsSandboxLayer()
NOROBOTS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NOROBOTS_FIXTURE, ),
                       name="collective.z3cform.norobots:Integration")