# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope


class NorobotsSandboxLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML, install the products and call its initialize() function
        # Load ZCML for this package
        import collective.z3cform.norobots

        self.loadZCML(package=collective.z3cform.norobots)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.z3cform.norobots:default")

    def tearDownPloneSite(self, portal):
        applyProfile(portal, "collective.z3cform.norobots:uninstall")

    def tearDownZope(self, app):
        zope.uninstallProduct(app, "collective.z3cform.norobots")


NOROBOTS_FIXTURE = NorobotsSandboxLayer()
NOROBOTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(NOROBOTS_FIXTURE,),
    name="collective.z3cform.norobots:Integration",
)
NOROBOTS_FUNCTIONNAL_TESTING = FunctionalTesting(
    bases=(NOROBOTS_FIXTURE,),
    name="collective.z3cform.norobots:Integration",
)
