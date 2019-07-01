import unittest
import doctest
import six
import re

from plone.testing import layered

from collective.z3cform.norobots.testing import NOROBOTS_INTEGRATION_TESTING

class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                doctest.DocFileSuite(
                    'doctests.rst',
                    optionflags=
                        doctest.REPORT_ONLY_FIRST_FAILURE |
                        doctest.NORMALIZE_WHITESPACE |
                        doctest.ELLIPSIS,
                    checker=Py23DocChecker()
                ),
                layer=NOROBOTS_INTEGRATION_TESTING
            ),
        ]
    )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')