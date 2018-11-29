from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pycmx',
      version='0.1',
      author='Jamie Hardt',
      author_email='jamiehardt@me.com',
      description='CMX3600 Edit Decision List Parser',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/iluvcapra/pycmx',
      packages=['pycmx'])
