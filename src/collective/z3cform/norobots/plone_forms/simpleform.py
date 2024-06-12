from collective.z3cform.norobots.i18n import norobotsMessageFactory as _
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.interface import Interface


class ISimpleForm(Interface):
    fullname = schema.TextLine(
        title=_("Name"),
        description=_("Please enter your full name."),
        required=False,
    )


class SimpleForm(form.Form):
    fields = field.Fields(ISimpleForm)
    ignoreContext = True  # don't use context to get widget data
    id = "simpleform"

    @button.buttonAndHandler(_("Send"))
    def handle_send(self, action):
        data, errors = self.extractData()


class SimpleFormView(FormWrapper):

    form = SimpleForm

    index = ViewPageTemplateFile("simpleform-with-macro.pt")
