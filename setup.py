#!/usr/bin/env python3

from distutils.core import setup

setup(name='pwshow',
      version='1.0', #TODO: remove dup version from __init__.py
      author="Kandalintsev Alexandre",
      author_email='spam@messir.net',
      license="GPLv3",
      description="Your secure password manager",
      scripts=['pwshow.py']
)
