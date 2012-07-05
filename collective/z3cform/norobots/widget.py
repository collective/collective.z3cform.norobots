from zope.component import getMultiAdapter
import zope.interface
from z3c.form import interfaces as z3cFormInterfaces

from Acquisition import aq_inner
from z3c.form.browser import text
from z3c.form import widget

class INorobotsWidget(z3cFormInterfaces.IWidget):
    """Marker interface for th norobots widget
    """
    
    def get_question():
        """ """

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
