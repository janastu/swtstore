# -*- coding: utf-8 -*-
"""
    setup.py
    ~~~~~~~~

    :copyright: (c) 2014, swtstore authors. see AUTHORS file for more details.
    :license: BSD License, see LICENSE for more details.
"""

"""
swtstore
--------

The store for decentralized, semantic, social web tweets a.k.a SWeeTs!!

"""
from setuptools import setup

requires = [
    'Flask==0.10.1',
    'Flask-SQLAlchemy==1.0',
    'sqlalchemy==0.9.4',
    'Flask-OAuthlib',
    'requests'
]


setup(
    name='swtstore',
    version='0.1 - alpha',
    url='https://github.com/janastu/swtstore',
    license='BSD',
    author='swtstore authors',
    author_email='anon@servelots.com',
    description='Server-side store for decentralized, semantic, social, web\
                tweets',
    long_description=__doc__,
    packages=['swtstore'],
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Social :: Semantic :: Decentralized',
    ]
)
