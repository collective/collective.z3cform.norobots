Introduction
============

collective.z3cform.norobots provides a "human" captcha widget based on a list of
questions/answers.

This captcha can be used as a plone.app.discussiom captcha plugin.

The widget is based on z3c.form.TextWidget.

Requirements
============

 * tested with Plone 4.0 as a plugin for plone.app.discussion, should work with Plone 3
 * plone.app.z3cform

Installation
============

Just a simple easy_install collective.z3cform.norobots is enough.

Alternatively, buildout users can install collective.z3cform.norobots as part of
a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs =
            collective.z3cform.norobots
        ...
        [instance]
        ...
        zcml =
            collective.z3cform.norobots


In portal_setup, apply the profile collective.z3cform.norobots:default.

Add a new question
===================

In the Plone Property Sheet "norobots_properties" (portal_properties/norobots_properties), add a new property:
::

   Name: The question id (ex: "question4")
   Value: your_question::the_answer (ex: "What is 10 + 12 ?::22")
   Type: string

Answer can contain multiple values delimited by semicolon:
::

   Name: The question id (ex: "question8")
   Value: your_question::the_answer;another_answer (ex: "What is 5 + 5 ?::10;ten")
   Type: string

Usage
=====

You can use this widget setting the "widgetFactory" property of a form field:
::

        from zope import interface, schema
        from z3c.form import interfaces, form, field, button, validator
        from plone.app.z3cform.layout import wrap_form

        from collective.z3cform.norobots.i18n import MessageFactory as _
        from collective.z3cform.norobots.widget import NorobotsFieldWidget
        from collective.z3cform.norobots.validator import NorobotsValidator

        class INorobotsForm(interface.Interface):
            norobots = schema.TextLine(title=_(u'Are you a human ?'),
                                       description=_(u'In order to avoid spam, please answer the question below.'),
                                       required=True)

        class NorobotsForm(form.Form):
            fields = field.Fields(INorobotsForm)
            fields['norobots'].widgetFactory = NorobotsFieldWidget

        # wrap the form with plone.app.z3cform's Form wrapper
        NorobotsFormView = wrap_form(NorobotsForm)

        # Register Norobots validator for the correponding field in the IContactInfo interface
        validator.WidgetValidatorDiscriminators(NorobotsValidator, field=INorobotsForm['norobots'])

for more information see contact_info.py in the plone_forms directory in the
package.

Possible problems
-----------------

  * I have the following error: "We already have: zope.schema 3.5.4 but z3c.form 2.4.1 requires 'zope.schema>=3.6.0'."
    => You should add this extra version restriction to your buildout: http://good-py.appspot.com/release/plone.app.z3cform/0.5.0

  * I have the following error when launching the tests: "ImportError: No module named lxml.html"
    => In order to run the tests you need lxml. You can add for example 
    "z3c.form [test]" to your buildout. See http://plone.293351.n2.nabble.com/Custom-Dexterity-Widgets-td5594532.html for more details.

Credits
===============
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
