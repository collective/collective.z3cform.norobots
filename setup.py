import os

from setuptools import setup, find_packages

version = '1.3'


def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.txt'),
     read('docs', 'HISTORY.txt'),
    ]
)

tests_require = ['zope.app.testing',
                 'Products.PloneTestCase',
                 'lxml']

classifiers = [
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Python Modules"]

setup(
    name='collective.z3cform.norobots',
    namespace_packages=['collective', 'collective.z3cform'],
    version=version,
    description='Human readable captcha for z3cform',
    long_description=long_description,
    classifiers=classifiers,
    keywords='plone z3cform captcha',
    author='Sylvain Boureliou',
    author_email='sylvain.boureliou@makina-corpus.com',
    url='http://www.makina-corpus.com',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'plone.app.z3cform',
    ],
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
    },
    # define there your console scripts
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,

)
