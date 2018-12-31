from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pycmx',
      version='0.9',
      author='Jamie Hardt',
      author_email='jamiehardt@me.com',
      description='CMX 3600 Edit Decision List Parser',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/iluvcapra/pycmx',
      classifiers=['Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Topic :: Multimedia',
          'Topic :: Multimedia :: Video',
          'Topic :: Text Processing',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
          
          ],
      packages=['pycmx'])
