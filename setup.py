import os, sys

from setuptools import setup, find_packages

version = '1.0'

def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.txt'),
     read('docs', 'HISTORY.txt'),
    ]
)

classifiers = [
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Python Modules",]

setup(
    name='collective.z3cform.norobots',
    namespace_packages=['collective', 'collective.z3cform',],
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
    # define there your console scripts
    entry_points="""
    # -*- Entry points: -*-
    """,

)
