"""Setup script for Stone

See: https://github.com/NeuralSandwich/stone
"""

# To use a consistent encoding
# pylint: disable=redefined-builtin
from codecs import open
import os
import re

# Apparently you should always prefer setuptools over distutils
from setuptools import setup, find_packages

# pylint: disable=invalid-name
ROOT = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

requires = [
    'jinja2',
    'unidecode'
]


def get_version():
    """Extract version from stone module"""
    init = open(os.path.join(ROOT, 'stone', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


# Get the long description from the README file
with open(os.path.join(ROOT, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='stone-site',
      version=get_version(),

      description='Static site generator',
      long_description=long_description,
      long_description_content_type="text/x-rst",

      # The project's main homepage
      url='https://github.com/NeuralSandwich/stone',

      # Author's details
      author='Sean Jones',
      author_email='sean@half.systems',
      license='MIT',

      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          ],

      # What does this project relate to?
      keywords='web html markdown static content',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),

      # List run-time dependencies here.
      # https://packaging.python.org/en/latest/requirements.html
      install_requires=requires,
      extras_require={
          'dev': ['check-manifest'],
          'test': ['coverage'],
      },
      entry_points={
          'console_scripts': ['stone=stone.__main__:main']
      }
     )
