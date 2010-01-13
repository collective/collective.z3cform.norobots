from zope import interface, schema
from z3c.form import interfaces, form, field, button, validator
from plone.app.z3cform.layout import wrap_form

from Products.CMFCore.utils import getToolByName
from ZODB.POSException import ConflictError

from collective.z3cform.norobots.i18n import MessageFactory as _
from collective.z3cform.norobots.plone_forms import constraints
from collective.z3cform.norobots.widget import NorobotsFieldWidget
from collective.z3cform.norobots.validator import NorobotsValidator

class IContactInfo(interface.Interface):

    fullname = schema.TextLine(title=_(u'Name'),
                               description=_(u'Please enter your full name.'),
                               required=True)

    email = schema.TextLine(title=_(u'E-Mail'),
                            description=_(u'Please enter your e-mail address.'),
                            required=True,
                            constraint=constraints.isEmail)

    subject = schema.TextLine(title=_(u'Subject'),
                              description=_(u'Please enter the subject of the message you want to send.'),
                              required=True)

    message = schema.Text(title=_(u'Message'),
                          description=_(u'Please enter the message you want to send.'),
                          required=True)

    norobots = schema.TextLine(title=_(u'Are you a human ?'),
                               description=_(u'In order to avoid spam, please answer the question below.'),
                               required=True)

class ContactInfoForm(form.Form):
    fields = field.Fields(IContactInfo)
    fields['norobots'].widgetFactory = NorobotsFieldWidget

    ignoreContext = True # don't use context to get widget data
    label = _(u'Contact form')

    def updateWidgets(self):
        super(ContactInfoForm, self).updateWidgets()
        # fullname
        self.widgets['fullname'].size = 40
        self.widgets['fullname'].maxlength = 200
        # email
        self.widgets['email'].size = 40
        self.widgets['email'].maxlength = 200
        # subject
        self.widgets['subject'].size = 40
        self.widgets['subject'].maxlength = 200
        # message - TextAreaWidget
        self.widgets['message'].rows = 8

        # If the current user is authenticated, hide fullname and email fields
        mtool = getToolByName(self.context, 'portal_membership')
        sender = mtool.getAuthenticatedMember()
        if sender.getId() is not None:
            self.widgets['fullname'].mode = interfaces.HIDDEN_MODE
            self.widgets['email'].mode = interfaces.HIDDEN_MODE

    def update(self):
        mtool = getToolByName(self.context, 'portal_membership')
        sender = mtool.getAuthenticatedMember()

        # If the current user is authenticated, fill in fullname and email fields
        if sender.getId() is not None:
            fullname = sender.getProperty('fullname')
            self.request.form['form.widgets.fullname'] = u'%s'%fullname
            email = sender.getProperty('email')
            self.request.form['form.widgets.email'] = u'%s'%email

        super(ContactInfoForm, self).update()

    @button.buttonAndHandler(_(u'Send'))
    def handle_send(self, action):
        data, errors = self.extractData()

        if errors:
            portal_msg = _(u"""Please correct the indicated errors and don't forget to fill in the field "Are you a human ?".""")
            self.context.plone_utils.addPortalMessage(portal_msg, 'error')

        else:
            context = self.context
            REQUEST = self.request
            mtool = getToolByName(self.context, 'portal_membership')
            plone_utils = getToolByName(context, 'plone_utils')
            urltool = getToolByName(context, 'portal_url')
            portal = urltool.getPortalObject()

            # message
            subject = data['subject']
            message = data['message']
            encoding = portal.getProperty('email_charset')

            # from
            fullname = data['fullname']
            send_from_address = data['email']
            envelope_from = portal.getProperty('email_from_address') # webmaster email
            sender = mtool.getAuthenticatedMember()
            sender_id = "%s (%s), %s" % (fullname, sender.getId(), send_from_address)
            referer = REQUEST.get('referer', 'unknown referer')

            # to
            send_to_address = portal.getProperty('email_from_address')

            # render template and send email
            variables = {'send_from_address' : send_from_address,
                         'sender_id'         : sender_id,
                         'url'               : referer,
                         'subject'           : subject,
                         'message'           : message,
                         'encoding'          : encoding,
            }

            host = context.MailHost # plone_utils.getMailHost() (is private)
            try:
                message = context.author_feedback_template(context, **variables)
                result = host.secureSend(message, send_to_address, envelope_from, subject=subject, subtype='plain', charset=encoding, debug=False, From=send_from_address)
            except ConflictError:
                raise
            except: # TODO Too many things could possibly go wrong. So we catch all.
                exception = plone_utils.exceptionString()
                message = _(u'Unable to send mail: ${exception}',
                              mapping={u'exception' : exception})
                plone_utils.addPortalMessage(message, 'error')
                return False

            plone_utils.addPortalMessage(_(u'Mail sent.'))

# wrap the form with plone.app.z3cform's Form wrapper
ContactInfoView = wrap_form(ContactInfoForm)

# Register Norobots validator for the correponding field in the IContactInfo interface
validator.WidgetValidatorDiscriminators(NorobotsValidator, field=IContactInfo['norobots'])
