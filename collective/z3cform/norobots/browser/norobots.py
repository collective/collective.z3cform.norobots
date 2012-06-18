import md5
import random

from zope.component import getUtility
from zope.interface import implements
from Products.Five import BrowserView
from plone.registry.interfaces import IRegistry

from interfaces import INorobotsView

from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings


class NoRobotsQuestionsError(Exception):
    """ Raised when no questions have been created """


class Norobots(BrowserView):
    implements(INorobotsView)

    def _get_questions_list(self):
        # [('question_id', 'question', 'answer'), ...]
        registry = getUtility(IRegistry)
        norobots_settings = registry.forInterface(INorobotsWidgetSettings)
        norobots_questions = norobots_settings.questions

        questions = []
        
        for i in range(len(norobots_questions)):
            # values must be "question::answer1;answer2;...;answerN"
            item = norobots_questions[i]
            
            if '::' in item:
                question_id = 'question%d' % i
                question, answer = item.split('::')
                question, answer = question.strip(), answer.strip()
                answers = [a.strip().lower() for a in answer.split(';') if a.strip()]
                questions.append((question_id, question, answers))

        if not questions:
            raise NoRobotsQuestionsError

        return questions

    def _get_questions_dict(self):
        questions_dict = {}  # {'question_id': ('question', 'answer'), ...}
        for el in self._get_questions_list():
            questions_dict[el[0]] = (el[1], el[2])
        return questions_dict

    def get_question(self):
        # See interfaces/INorobotsView
        questions = self._get_questions_list()
        q_id, q_title, q_answers = random.sample(questions, 1)[0]
        id_check = md5.new(q_title).hexdigest()
        return {'id': q_id,
                'title': q_title,
                'id_check': id_check}

    def verify(self, input):
        # See interfaces/INorobotsView
        input = str(input).lower()
        form = self.request.form
        question_id = form['question_id']
        id_check = form['id_check']

        questions = self._get_questions_dict()
        title, answers = questions[question_id]
        if not (md5.new(title).hexdigest() == id_check and input in answers):
            return False
        return True
