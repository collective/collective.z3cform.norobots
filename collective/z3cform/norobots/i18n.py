from zope.i18nmessageid import MessageFactory
MessageFactory = MessageFactory('collective.z3cform.norobots')
_ = MessageFactory

def dummy_strings():
    """ Dummy i18n strings for default questions """
    question1 = _("What is 4 + 4 ?")
    question2 = _("What is 10 + 4 ?")
    question3 = _("Write five cipher.")

