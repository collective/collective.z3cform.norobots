import md5
import random
import logging
logger = logging.getLogger("collective.z3cform.norobots")

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

    def _hashTitle(self, title):
        return md5.new(title.encode('ascii', 'ignore')).hexdigest()

    def _get_questions_list(self):
        # [('question_id', 'question', 'answer'), ...]
        registry = getUtility(IRegistry)
        try:
            norobots_settings = registry.forInterface(INorobotsWidgetSettings)
            norobots_questions = norobots_settings.questions
        except KeyError:
            # Can occurs for this story:
            # 1) collective.z3cform.norobots's zcml is loaded
            # 2) The module IS NOT installed through the addons control panel
            # 3) The field is used in a z3c form or is configured as the plone.app.discussion's captcha
            # => FIX : install using the addons control panel
            logger.error("MODULE MUST BE INSTALLED")
            norobots_questions = ()

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
            #raise NoRobotsQuestionsError
            logger.error("QUESTIONS MUST BE CONFIGURED IN THE DEDICATED CONTROL PANEL")

        return questions

    def _get_questions_dict(self):
        questions_dict = {}  # {'question_id': ('question', 'answer'), ...}
        for el in self._get_questions_list():
            questions_dict[el[0]] = (el[1], el[2])
        return questions_dict

    def get_question(self):
        # See interfaces/INorobotsView
        questions = self._get_questions_list()
        if questions:
            q_id, q_title, q_answers = random.sample(questions, 1)[0]
            id_check = self._hashTitle(q_title)
            return {'id': q_id,
                    'title': q_title,
                    'id_check': id_check}
        else:
            return {'id': '',
                    'title': '',
                    'id_check': ''}
            

    def verify(self, input, question_id=None, id_check=None):
        # See interfaces/INorobotsView
        
        # user's answer
        input = str(input).lower()
        
        # question id and is corresponding id check
        form = self.request.form
        
        if question_id is None:
            question_id = form.get('question_id', '')
        
        if id_check is None:
            id_check = form.get('id_check', '')

        # verify the answer
        questions = self._get_questions_dict()
        title, answers = questions.get(question_id, ('', ''))
        
        if not (self._hashTitle(title) == id_check and input in answers):
            return False
        return True
