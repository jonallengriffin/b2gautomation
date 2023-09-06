import os
from setuptools import setup, find_packages

version = '0.1'

# get documentation from the README
try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.md')).read()
except (OSError, IOError):
    description = 'b2g automation scripts'

# dependencies
deps = ['GitPython == 3.1.34', 'mozprocess']

setup(name='b2gautomation',
      version=version,
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla b2g',
      author='Jonathan Griffin',
      author_email='jgriffin@mozilla.com',
      url='https://github.com/jonallengriffin/b2gautomation',
      license='MPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      )

