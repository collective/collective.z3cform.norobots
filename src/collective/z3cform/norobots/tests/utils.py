def getPloneVersion():
    try:
        # Plone 4.1 and higher 
        import plone.app.caching
        HAS_PLONE_APP_CACHING = True
    except:
        HAS_PLONE_APP_CACHING = False
    
    try:
        # Plone 4.2 and higher 
        import plone.app.collection
        HAS_PLONE_APP_COLLECTION = True
    except:
        HAS_PLONE_APP_COLLECTION = False
    
    try:
        # Plone 4.3 and higher 
        import plone.app.dexterity
        HAS_PLONE_APP_DEXTERITY = True
    except:
        HAS_PLONE_APP_DEXTERITY = False
    
    if HAS_PLONE_APP_DEXTERITY:
        PLONE_VERSION = 4.3
    elif HAS_PLONE_APP_COLLECTION:
        PLONE_VERSION = 4.2
    elif HAS_PLONE_APP_CACHING:
        PLONE_VERSION = 4.1
    else:
        PLONE_VERSION = 4.0
    
    return PLONE_VERSION


PLONE_VERSION = getPloneVersion()
print 'PLONE_VERSION ===================> %s' % PLONE_VERSION