from pkg_resources import get_distribution

PLONE_VERSION = get_distribution('Products.CMFPlone').version
