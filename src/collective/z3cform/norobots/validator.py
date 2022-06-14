# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.z3cform.norobots.i18n import norobotsMessageFactory as _
from z3c.form import validator
from zope.component import getMultiAdapter
from zope.schema import ValidationError


class WrongNorobotsAnswer(ValidationError):
    __doc__ = _("""You entered a wrong answer, please answer the new question below.""")


class NorobotsValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super().validate(value)
        norobots = getMultiAdapter(
            (aq_inner(self.context), self.request),
            name="norobots",
        )
        if norobots.verify(value):
            return True
        raise WrongNorobotsAnswer
