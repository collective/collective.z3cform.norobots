from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.z3cform.norobots.browser.interfaces import INorobotsWidgetSettings

PROFILEID = 'profile-collective.z3cform.norobots:default'

def upgrade_to_2(context):
    
    # Run the default profile
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILEID)

    # Copy questions from the old property sheet to the registry
    # then delete the property sheet
    portal_properties = getToolByName(context, 'portal_properties')
    if hasattr(portal_properties, 'norobots_properties'):
        
        # Get question from the property sheet
        props = portal_properties.norobots_properties
        questions = []
        for item in props.propertyItems():
            # values must be "question::answer1;answer2;...;answerN"
            if item[0] != 'title':
                questions.append(u'%s' % item[1])
        
        # Save question in the registry
        registry = getUtility(IRegistry)
        norobots_settings = registry.forInterface(INorobotsWidgetSettings)
        norobots_settings.questions = tuple(questions)
        
        # Delete the old property sheet
        portal_properties.manage_delObjects('norobots_properties')

    