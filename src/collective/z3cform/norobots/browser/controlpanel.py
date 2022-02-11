# -*- coding: utf-8 -*-
from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings
from collective.z3cform.norobots.i18n import norobotsMessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout


class NorobotsControlPanelForm(RegistryEditForm):
    schema = INorobotsWidgetSettings

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["questions"].rows = 15


NorobotsControlPanelView = layout.wrap_form(
    NorobotsControlPanelForm, ControlPanelFormWrapper
)
NorobotsControlPanelView.label = _("Norobots widget settings")
