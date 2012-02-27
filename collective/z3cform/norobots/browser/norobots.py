import md5
import random

from zope.interface import implements
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from interfaces import INorobotsView


class NoRobotsQuestionsError(Exception):
    """ Raised when no questions have been created in portal_properties/norobots_properties """


class Norobots(BrowserView):
    implements(INorobotsView)

    def _get_questions_list(self):
        # [('question_id', 'question', 'answer'), ...]
        portal_properties = getToolByName(self.context, 'portal_properties')
        props = portal_properties.norobots_properties

        questions = []
        for item in props.propertyItems():
            # values must be "question::answer1;answer2;...;answerN"
            if item[0] != 'title' and '::' in item[1]:
                question, answer = item[1].split('::')
                answers = [a.strip().lower() for a in answer.split(';') if a.strip()]
                questions.append((item[0], question, answers))

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
        input = input.lower()
        form = self.request.form
        question_id = form['question_id']
        id_check = form['id_check']

        questions = self._get_questions_dict()
        title, answers = questions[question_id]
        if not (md5.new(title).hexdigest() == id_check and input in answers):
            return False
        return True
