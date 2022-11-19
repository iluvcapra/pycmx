from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pycmx',
      version='1.1.5',
      author='Jamie Hardt',
      author_email='jamiehardt@me.com',
      description='CMX 3600 Edit Decision List Parser',
      long_description_content_type="text/markdown",
      long_description=long_description,
      project_urls={
          'Source':
              'https://github.com/iluvcapra/pycmx',
          'Documentation':
              'https://pycmx.readthedocs.io/',
          'Issues':
              'https://github.com/iluvcapra/pycmx/issues',
      },
      url='https://github.com/iluvcapra/pycmx',
      classifiers=['Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Multimedia',
          'Topic :: Multimedia :: Video',
          'Topic :: Text Processing',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10'
          ],
      packages=['pycmx'])
