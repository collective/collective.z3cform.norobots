from Acquisition import aq_inner

from zope.component import getMultiAdapter
from zope.schema import ValidationError

from z3c.form import validator

from collective.z3cform.norobots.i18n import MessageFactory as _


class WrongNorobotsAnswer(ValidationError):
    __doc__ = _("""You entered a wrong answer, please answer the new question below.""")


class NorobotsValidator(validator.SimpleFieldValidator):

    def validate(self, value):
        super(NorobotsValidator, self).validate(value)
        norobots = getMultiAdapter((aq_inner(self.context), self.request), name='norobots')
        if norobots.verify(value):
            return True
        raise WrongNorobotsAnswer
