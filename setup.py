import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(name="django-monfhir",
      version="0.0.0.9",
      license='GPL2', 
      packages=['monfhir', 'monfhir.views',],
      description="A FHIR Server as a reusable Django apps. (Requires MongoDB)",
      long_description=README,
      author="Alan Viars (contributions - Mark Scrimshire)",
      author_email="sales@videntity.com",
      url="https://github.com/transparenthealth/django-monfhir",
      download_url="https://github.com/transparenthealth/django-monfhir/tarball/master",
      install_requires=[
        'django>1.8', 'django-oauth-toolkit-scopes-backend',
        'django-cors-headers', 'jsonschema', 'pymongo'],
      include_package_data=True,
      scripts=[],
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

      )


