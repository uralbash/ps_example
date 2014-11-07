import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(here, name)) as f:
        return f.read()

setup(name='pyramid_sacrud_example',
      version='0.0.3',
      description='Pyramid sacrud example',
      long_description=read('README.rst') + '\n\n' + read('CHANGES.txt'),
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyramid_sacrud_example',
      entry_points="""\
      [paste.app_factory]
      main = pyramid_sacrud_example:main
      [console_scripts]
      initialize_example_db = pyramid_sacrud_example.scripts.initializedb:main
      """,
      )
