NoRobots widget
================

collective.z3cform.norobots provides a "human" captcha widget based on a list of
questions/answers.

A z3cform implementation for the Plone contact form is available in
browser/plone_forms .

    >>> from collective.z3cform.norobots.widget import NorobotsFieldWidget
    >>> from collective.z3cform.norobots.widget import NorobotsWidget
    >>> from collective.z3cform.norobots.validator import NorobotsValidator
    >>> from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings

	>>> from zope.component import getUtility
    >>> from plone.registry.interfaces import IRegistry
    
    >>> app = layer['app']
    >>> portal = layer['portal']
    >>> request = layer['request']
    
    >>> registry = getUtility(IRegistry)
    >>> norobots_settings = registry.forInterface(INorobotsWidgetSettings)

Remove default questions added when installing the product:

   >>> norobots_settings.questions = ()

First, set up a simple test form and context:

    >>> from z3c.form import testing
    >>> testing.setupFormDefaults()

    >>> import zope.interface
    >>> import zope.schema
    >>> from zope.schema.fieldproperty import FieldProperty

    >>> class IFooForm(zope.interface.Interface):
    ...     id = zope.schema.TextLine(title=u'ID', readonly=True, required=True)
    ...     norobots = zope.schema.TextLine(title=u'Are you a human ?',
    ...                                     required=True)

Let's now create a form that implements our interface and specify the
NorobotsWidget factory ('NorobotsFieldWidget') as the field's widgetFactory:

    >>> from z3c.form.testing import TestRequest
    >>> from zope.interface import alsoProvides
    >>> from zope.annotation.interfaces import IAttributeAnnotatable

    >>> from z3c.form import form, field, validator
    >>> from plone.app.z3cform.layout import wrap_form

    >>> class FooForm(form.Form):
    ...     fields = field.Fields(IFooForm)
    ...     fields['norobots'].widgetFactory = NorobotsFieldWidget
    ...     ignoreContext = True
    ...     label = u'Foo form'

Register Norobots validator for the correponding field in the IFooForm interface:

    >>> from zope.component import provideAdapter
    >>> validator.WidgetValidatorDiscriminators(NorobotsValidator, field=IFooForm['norobots'])
    >>> provideAdapter(NorobotsValidator)

Create an empty form:

    >>> request = TestRequest()
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

Check for the norobots widget:

    >>> foo_form.widgets.keys()
    ['id', 'norobots']

    >>> foo_form.widgets['norobots'].field # doctest: +ELLIPSIS
    <zope.schema._bootstrapfields.TextLine object at ...>

A widget with an empty captcha is rendered if there is no question/answer:

    # Tthe widget may be rendered differently but it is always the same (depends on the Plone version)
    >>> foo_form.widgets['norobots'].render() in [
    ...       u'\n\t\n  <strong><span>Question</span></strong>:\n  <span></span><br />\n\n  <strong><span>Your answer</span></strong>:\n  \n  <input type="text" id="form-widgets-norobots" name="form.widgets.norobots" class="text-widget required textline-field" size="30" maxlength="200" value="" />\n                     \n  <input type="hidden" name="question_id" value="" />\n  <input type="hidden" name="id_check" value="" />\n         \n'
    ...       ]
    True

and if the form is submitted the validation failed:

    >>> request = TestRequest(form={
    ...     'question_id': '',
    ...     'id_check': '',
    ...     'form.widgets.norobots': u'an answer'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    (<ErrorViewSnippet for WrongNorobotsAnswer>,)
    >>> errors[0].message
    u'You entered a wrong answer, please answer the new question below.'

Define a first question. Each question with be a string like this: "The question::The answer".

    >>> question_1 = u'Hé, What is 10 + 4?' # include a non-ascii char
    >>> answer_1 = u'14'
    >>> norobots_settings.questions = (u'%s::%s' % (question_1, answer_1),)

Render the widget:

Note that the returned question is selected randomly from the available
question, but we actually have only one question, so:

    # The widget may be rendered differently but it is always the same (depends on the Plone version)
    >>> foo_form.widgets['norobots'].render() in [
    ...       u'\n\t\n  <strong><span>Question</span></strong>:\n  <span>H\xc3\xa9, What is 10 + 4?</span><br />\n\n  <strong><span>Your answer</span></strong>:\n  \n  <input type="text" id="form-widgets-norobots" name="form.widgets.norobots" class="text-widget required textline-field" size="30" maxlength="200" value="" />\n                     \n  <input type="hidden" name="question_id" value="question0" />\n  <input type="hidden" name="id_check" value="d382e1617bad3a3380d355985878bf62" />\n         \n'
    ...       ]
    True
    >>> temp_id_check = 'd382e1617bad3a3380d355985878bf62'

Submit the form with a bad answer:

    >>> request = TestRequest(form={
    ...     'question_id': 'question0',
    ...     'id_check': temp_id_check,
    ...     'form.widgets.norobots': u'bad answer'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    (<ErrorViewSnippet for WrongNorobotsAnswer>,)
    >>> errors[0].message
    u'You entered a wrong answer, please answer the new question below.'

Submit the form with a good answer:

    >>> request = TestRequest(form={
    ...     'question_id': 'question0',
    ...     'id_check': temp_id_check,
    ...     'form.widgets.norobots': u'14'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()

Submit the form with a bad id_check:

    >>> request = TestRequest(form={
    ...     'question_id': 'question0',
    ...     'id_check': 'BAD-%s' % temp_id_check,
    ...     'form.widgets.norobots': u'14'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    (<ErrorViewSnippet for WrongNorobotsAnswer>,)
    >>> errors[0].message
    u'You entered a wrong answer, please answer the new question below.'

Test that the rendered question is not always the same:

    >>> # add 20 questions (we already have one question, so add question1 -> question20)
    >>> questions = list(norobots_settings.questions)
    >>> for i in range(20):
    ...     question = u'question %d' % (i+1)
    ...     answer = u'answer %d' % (i+1)
    ...     questions.append(u'%s::%s' % (question, answer))
    >>> norobots_settings.questions = tuple(questions)

    >>> # render the widget 20 times and check that it is not always the same
    >>> L = []
    >>> for i in range(20):
    ...     request = TestRequest()
    ...     alsoProvides(request, IAttributeAnnotatable)
    ...     foo_form = FooForm(portal, request)
    ...     foo_form.update()
    ...     html = foo_form.widgets['norobots'].render()
    ...     if html not in L:
    ...         L.append(html)

    >>> len(L) > 1
    True

Let's define a question (id=question21) in different formats which supports more than one answer per question.
Answers must be semicolon delimited and are case-normalized to lowercase before validation.
Example: "What is 5+5?::10; ten".

    >>> question = u'What is 5+5 ?'
    >>> answer = u'10; ten'
    >>> questions = list(norobots_settings.questions)
    >>> questions.append(u'%s::%s' % (question, answer))
    >>> norobots_settings.questions = tuple(questions)
    >>> temp_id_check = 'd18f7fcb669087ae51905a05875e94f3'

    >>> request = TestRequest(form={
    ...     'question_id': 'question21',
    ...     'id_check': temp_id_check,
    ...     'form.widgets.norobots': u'10'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()

    >>> request = TestRequest(form={
    ...     'question_id': 'question21',
    ...     'id_check': temp_id_check,
    ...     'form.widgets.norobots': u'ten'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()

    >>> request = TestRequest(form={
    ...     'question_id': 'question21',
    ...     'id_check': temp_id_check,
    ...     'form.widgets.norobots': u'TEN'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()
