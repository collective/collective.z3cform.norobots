from setuptools import find_packages
from setuptools import setup

import os


version = "3.0"


def read(*rnames):
    return open(os.path.join(".", *rnames)).read()


long_description = "\n\n".join([read("README.rst"), read("CHANGES.rst")])

setup(
    name="collective.z3cform.norobots",
    version=version,
    description="Human readable captcha for z3cform",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
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
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "plone.app.registry",
        "plone.registry",
        "plone.restapi",
        "Zope",
        "Products.CMFPlone",
        "Products.GenericSetup",
        "z3c.form",
        "plone.base",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.api",
            "plone.app.testing",
            "plone.browserlayer",
            "plone.testing>=5.0.0",
            "six",
            "lxml",
        ]
    },
    test_suite="collective.z3cform.norobots.tests.test_docs.test_suite",
    # define there your console scripts
    entry_points={"z3c.autoinclude.plugin": "target = plone"},
)
