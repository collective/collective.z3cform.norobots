# -*- coding: utf-8 -*-
from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings
from collective.z3cform.norobots.i18n import _
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, Interface)
class NoRobotsSettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = INorobotsWidgetSettings
    configlet_id = "collective.z3cform.norobots.settings"
    configlet_category_id = "Products"
    title = _("NoRobots Settings Control Panel")
    group = ""
    schema_prefix = (
        "collective.z3cform.norobots.browser.interfaces.INorobotsWidgetSettings"
    )
