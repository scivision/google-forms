#!/usr/bin/env python
install_requires=['pandas']
tests_require=['nose','coveralls']
# %%
from setuptools import setup, find_packages

setup(name='google-forms',
      packages=find_packages(),
      description ='Analyze Blackboard and Google Forms results',
      author = 'Michael Hirsch, Ph.D.',
      version = '0.5.0',
      url = 'https://github.com/scivision/google-forms',
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      ],
      install_requires=install_requires,
      python_requires='>=3.6',
      tests_require=tests_require,
      extras_require={'tests':tests_require},
	  )
