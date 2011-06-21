#!/usr/bin/env python           
                                
# from distutils.core import setup
from setuptools import setup, find_packages
         
VERSION='0.0.2'

setup(name='livedoor-auth',
      version=VERSION,
      packages = find_packages(),
      py_modules=['livedoor'],

      install_requires = ['json-py'],

      package_data = {
          '' : ['README', 'example']
      },

      author='TANIGUCHI Takaki',             
      author_email='takaki@asis.media-as.org',                
      description='livedoor Auth API',
      license = "LGPL",
      keywords = "authentication",
      url='http://sourceforge.jp/projects/pyldauth',
     )
