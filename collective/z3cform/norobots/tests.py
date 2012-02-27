import unittest

import zope.testing
import zope.testing.doctest
import zope.component
from zope.app.testing import setup

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite(
                   extension_profiles=['collective.z3cform.norobots:testing'],
                   )

import collective.z3cform.norobots

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(test):
            pass

        @classmethod
        def tearDown(test):
            setup.placefulTearDown()

optionflags = (zope.testing.doctest.REPORT_ONLY_FIRST_FAILURE |
               zope.testing.doctest.ELLIPSIS |
               zope.testing.doctest.NORMALIZE_WHITESPACE
               )


def test_suite():
    return unittest.TestSuite((
        ztc.FunctionalDocFileSuite(
            'README.txt',
            package='collective.z3cform.norobots',
            test_class=TestCase,
            optionflags=optionflags),
        ))
