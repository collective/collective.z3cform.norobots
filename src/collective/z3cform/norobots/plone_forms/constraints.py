# Helper functions for fields validation

import re

from zope import schema

from collective.z3cform.norobots.i18n import MessageFactory as _

class IsEmailError(schema.ValidationError):
    __doc__ = _("""You entered an invalid email address.""")

def isEmail(value):
    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$", re.IGNORECASE)
    if expr.match(value):
        return True
    raise IsEmailError
