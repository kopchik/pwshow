#!/usr/bin/env python3

from distutils.core import setup
from pwshow import __version__

setup(name='pwshow',
      version=__version__,
      author="Kandalintsev Alexandre",
      author_email='spam@messir.net',
      license="GPLv3",
      description="Your secure password manager",
      scripts=['pwshow.py']
)
