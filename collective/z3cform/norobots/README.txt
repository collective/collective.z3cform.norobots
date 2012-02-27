NoRobots widget
================

collective.z3cform.norobots provides a "human" captcha widget based on a list of
questions/answers.

A z3cform implementation for the Plone contact form is available in
browser/plone_forms .

    >>> from collective.z3cform.norobots.widget import NorobotsFieldWidget
    >>> from collective.z3cform.norobots.widget import NorobotsWidget
    >>> from collective.z3cform.norobots.validator import NorobotsValidator

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

A NoRobotsQuestionsError error is raised if there is no question/answer:

    >>> foo_form.widgets['norobots'].render() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    NoRobotsQuestionsError

Define a first question in the property sheet "norobots_properties". Each
question with be a string like this: "The question::The answer".

    >>> from Products.CMFCore.utils import getToolByName
    >>> portal_properties = getToolByName(portal, 'portal_properties')
    >>> props = portal_properties.norobots_properties

    >>> question_id = 'question1'
    >>> question = 'What is 10 +4 ?'
    >>> answer = '14'
    >>> props.manage_addProperty(question_id, '%s::%s'%(question, answer), 'string')

Render the widget:

Note that the returned question is selected randomly from the available
question, but we actually have only one question, so:

    # In Plone 4 with plone.app.z3cform 0.5.0 the widget is rendered differently but it is always the same (this is the second one in the list bellow)
    >>> foo_form.widgets['norobots'].render() in [
    ...       u'\n\n  <input type="hidden" name="question_id" value="question1" />\n  <input type="hidden" name="id_check"\n         value="741a211ffff0a652efa89fb89c790fc6" />\n\n  <strong><span>Question</span></strong>:\n  <span>What is 10 +4 ?</span><br />\n\n  <strong><span>Your answer</span></strong>:\n  <input type="text" id="form-widgets-norobots"\n         name="form.widgets.norobots"\n         class="text-widget required textline-field"\n         size="30" maxlength="200" value="" />\n\n\n',
    ...       u'\n\n  <input type="hidden" name="question_id" value="question1" />\n  <input type="hidden" name="id_check" value="741a211ffff0a652efa89fb89c790fc6" />\n\n  <strong><span>Question</span></strong>:\n  <span>What is 10 +4 ?</span><br />\n\n  <strong><span>Your answer</span></strong>:\n  <input type="text" id="form-widgets-norobots" name="form.widgets.norobots" class="text-widget required textline-field" size="30" maxlength="200" value="" />\n\n\n'
    ...       ]
    True

Submit the form with a bad answer:

    >>> request = TestRequest(form={
    ...     'question_id': 'question1',
    ...     'id_check': '741a211ffff0a652efa89fb89c790fc6',
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
    ...     'question_id': 'question1',
    ...     'id_check': '741a211ffff0a652efa89fb89c790fc6',
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
    ...     'question_id': 'question1',
    ...     'id_check': 'BAD-741a211ffff0a652efa89fb89c790fc6',
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

    >>> # add 20 questions
    >>> for i in range(20):
    ...     question_id = 'q%d' % i
    ...     question = 'question %d' % i
    ...     answer = 'answer %d' % i
    ...     props.manage_addProperty(question_id, '%s::%s'%(question, answer), 'string')

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

Let's define a question in different formats which supports more than one answer per question.
Answers must be semicolon delimited and are case-normalized to lowercase before validation.
Example: "What is 5+5?::10; ten".

    >>> question_id = 'question2'
    >>> question = 'What is 5+5 ?'
    >>> 
    >>> answer = '10; ten'
    >>> props.manage_addProperty(question_id, '%s::%s'%(question, answer), 'string')

    >>> request = TestRequest(form={
    ...     'question_id': 'question2',
    ...     'id_check': 'd18f7fcb669087ae51905a05875e94f3',
    ...     'form.widgets.norobots': u'10'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()

    >>> request = TestRequest(form={
    ...     'question_id': 'question2',
    ...     'id_check': 'd18f7fcb669087ae51905a05875e94f3',
    ...     'form.widgets.norobots': u'ten'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()

    >>> request = TestRequest(form={
    ...     'question_id': 'question2',
    ...     'id_check': 'd18f7fcb669087ae51905a05875e94f3',
    ...     'form.widgets.norobots': u'TEN'}
    ...     )
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> foo_form = FooForm(portal, request)
    >>> foo_form.update()

    >>> data, errors = foo_form.extractData()
    >>> errors
    ()
