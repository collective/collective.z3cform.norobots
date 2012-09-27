from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings
from plone.z3cform import layout

from collective.z3cform.norobots.i18n import norobotsMessageFactory as _

class NorobotsControlPanelForm(RegistryEditForm):
    schema = INorobotsWidgetSettings
    
    def updateWidgets(self):
        super(NorobotsControlPanelForm, self).updateWidgets()
        self.widgets['questions'].rows = 15

NorobotsControlPanelView = layout.wrap_form(NorobotsControlPanelForm, ControlPanelFormWrapper)
NorobotsControlPanelView.label = _(u"Norobots widget settings")