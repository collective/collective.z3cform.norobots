from zope.component import getMultiAdapter
import zope.interface

from Acquisition import aq_inner
from z3c.form.browser import text
from z3c.form import widget

from interfaces import INorobotsWidget


class NorobotsWidget(text.TextWidget):
    maxlength = 200
    size = 30

    zope.interface.implementsOnly(INorobotsWidget)

    def get_question(self):
        # return a dictionary {'id': '...', 'title': '...', 'id_check': '...'}
        self.norobots = getMultiAdapter((aq_inner(self.context), self.request), name='norobots')
        return self.norobots.get_question()


def NorobotsFieldWidget(field, request):
    """IFieldWidget factory for NorobotsWidget."""
    return widget.FieldWidget(field, NorobotsWidget(request))
