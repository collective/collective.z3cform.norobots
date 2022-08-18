# -*- coding: utf-8 -*-
from collective.z3cform.norobots.i18n import norobotsMessageFactory as _
from collective.z3cform.norobots.plone_forms import constraints
from collective.z3cform.norobots.validator import NorobotsValidator
from collective.z3cform.norobots.widget import NorobotsFieldWidget
from plone.app.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form import validator
from zope import interface
from zope import schema


class IContactInfo(interface.Interface):

    fullname = schema.TextLine(
        title=_("Name"),
        description=_("Please enter your full name."),
        required=False,
    )

    email = schema.TextLine(
        title=_("E-Mail"),
        description=_("Please enter your e-mail address."),
        required=True,
        constraint=constraints.isEmail,
    )

    subject = schema.TextLine(
        title=_("Subject"),
        description=_("Please enter the subject of the message you want to send."),
        required=True,
    )

    message = schema.Text(
        title=_("Message"),
        description=_("Please enter the message you want to send."),
        required=True,
    )

    norobots = schema.TextLine(
        title=_("Are you a human ?"),
        description=_("In order to avoid spam, please answer the question below."),
        required=True,
    )


class ContactInfoForm(form.Form):
    fields = field.Fields(IContactInfo)
    fields["norobots"].widgetFactory = NorobotsFieldWidget

    ignoreContext = True  # don't use context to get widget data
    id = "z3cform_contact_info_form"
    label = _("Contact form")

    def updateWidgets(self):
        super().updateWidgets()
        # fullname
        self.widgets["fullname"].size = 40
        self.widgets["fullname"].maxlength = 200
        # email
        self.widgets["email"].size = 40
        self.widgets["email"].maxlength = 200
        # subject
        self.widgets["subject"].size = 40
        self.widgets["subject"].maxlength = 200
        # message - TextAreaWidget
        self.widgets["message"].rows = 8

    def update(self):
        mtool = getToolByName(self.context, "portal_membership")
        sender = mtool.getAuthenticatedMember()

        # If the current user is authenticated, fill in fullname and email fields
        if sender.getId() is not None:
            fullname = sender.getProperty("fullname")
            self.request.form["form.widgets.fullname"] = "%s" % fullname
            email = sender.getProperty("email")
            self.request.form["form.widgets.email"] = "%s" % email

        super().update()

    @button.buttonAndHandler(_("Send"))
    def handle_send(self, action):
        data, errors = self.extractData()

        if errors:
            portal_msg = _(
                """Please correct the indicated errors and don't forget to fill in the field 'Are you a human ?'."""
            )
            self.context.plone_utils.addPortalMessage(portal_msg, "error")
            return

        context = self.context

        plone_utils = getToolByName(context, "plone_utils")
        plone_utils.addPortalMessage("[FAKE] %s" % _("Mail sent."))


# wrap the form with plone.app.z3cform's Form wrapper
ContactInfoView = wrap_form(ContactInfoForm)

# Register Norobots validator for the correponding field in the IContactInfo interface
validator.WidgetValidatorDiscriminators(
    NorobotsValidator, field=IContactInfo["norobots"]
)
