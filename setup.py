# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


version = "2.1"


def read(*rnames):
    return open(os.path.join(".", *rnames)).read()


long_description = "\n\n".join([read("README.rst"), read("CHANGES.rst")])

tests_require = ["plone.app.testing"]

classifiers = [
    "Framework :: Plone",
    "Framework :: Plone :: 6.0",
    "Framework :: Plone :: 5.2",
    "Framework :: Plone :: 5.1",
    "Framework :: Plone :: 4.3",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="collective.z3cform.norobots",
    version=version,
    description="Human readable captcha for z3cform",
    long_description=long_description,
    classifiers=classifiers,
    keywords="plone z3cform captcha",
    author="Sylvain Boureliou",
    author_email="sylvain.boureliou@makina-corpus.com",
    url="http://www.makina-corpus.com",
    license="GPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["collective", "collective.z3cform"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "plone.app.z3cform",
        "plone.app.registry",
        "plone.api",
    ],
    tests_require=tests_require,
    test_suite="collective.z3cform.norobots.tests.test_docs.test_suite",
    extras_require={"test": tests_require},
    # define there your console scripts
    entry_points={"z3c.autoinclude.plugin": "target = plone"},
)
