import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(here, name)) as f:
        return f.read()

setup(name='ps_example',
      version='0.0.4.dev1',
      description='Pyramid sacrud example',
      long_description=read('README.rst'),
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='ps_example',
      entry_points="""\
      [paste.app_factory]
      main = ps_example:main
      [console_scripts]
      initialize_example_db = ps_example.scripts.initializedb:main
      """,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      )
