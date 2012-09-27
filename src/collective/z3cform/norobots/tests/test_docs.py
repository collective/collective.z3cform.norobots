import unittest
import doctest

from plone.testing import layered

from collective.z3cform.norobots.testing import NOROBOTS_INTEGRATION_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('doctests.rst',
                                     optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                                                 doctest.NORMALIZE_WHITESPACE | 
                                                 doctest.ELLIPSIS), 
                layer=NOROBOTS_INTEGRATION_TESTING),
    ])
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
