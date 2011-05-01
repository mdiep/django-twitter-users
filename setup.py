#!/usr/bin/env python
from setuptools import setup, find_packages
import os, re

PKG="twitter_users"
verstr="0.1.1"

setup(name=PKG,
      version=verstr,
      description="Django app for Twitter authentication",
      author="Matt Diephouse",
      author_email="matt@diephouse.com",
      url="https://github.com/mdiep/django-twitter-users",
      packages = find_packages(),
      install_requires = ['Django', 'oauth2'],
      license = "BSD3",
      keywords="oauth",
      zip_safe = True
      )
