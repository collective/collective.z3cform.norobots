try: 
    # Plone 4.1 and higher 
    import plone.app.caching
    PLONE_VERSION = 4.1
    print 'PLONE_VERSION ===================> 4.1'
except ImportError: 
    PLONE_VERSION = 4.0
    print 'PLONE_VERSION ===================> 4.0'