from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implementer_only

from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget

class INorobotsWidget(IWidget):
    """Marker interface for th norobots widget
    """

    def get_question():
        """ """
@implementer_only(INorobotsWidget)
class NorobotsWidget(TextWidget):

    maxlength = 200
    size = 30

    def get_question(self):
        # return a dictionary {'id': '...', 'title': '...', 'id_check': '...'}
        self.norobots = getMultiAdapter((aq_inner(self.context), self.request), name='norobots')
        return self.norobots.get_question()

def NorobotsFieldWidget(field, request):
    """IFieldWidget factory for NorobotsWidget."""
    return FieldWidget(field, NorobotsWidget(request))
