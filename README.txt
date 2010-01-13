Introduction
============

collective.z3cform.norobots provides a "human" captcha widget based on a list of
questions/answers.

The widget is based on z3c.form.TextWidget.

Requirements
------------
 * tested with Plone 3.3.2
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
