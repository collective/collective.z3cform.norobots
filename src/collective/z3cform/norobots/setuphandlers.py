# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            "collective.z3cform.norobots:uninstall",
        ]


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
