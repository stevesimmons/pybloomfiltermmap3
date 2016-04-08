import os
import sys

from setuptools import setup, Extension
from Cython.Distutils import build_ext

here = os.path.dirname(__file__)

ext_files = [
  'src/mmapbitarray.c',
  'src/bloomfilter.c',
  'src/md5.c',
  'src/primetester.c',
  'src/MurmurHash3.c',
  'src/pybloomfilter.pyx'
]

sys.path.insert(0, os.path.join(here, 'fake_pyrex'))

print("info: Building from Cython")

ext_modules = [
  Extension("pybloomfilter", ext_files, libraries=['crypto'])
]

if sys.version_info[0] < 3:
  raise SystemError('This Package is for Python Version 3 and above.')

setup(
  name='pybloomfiltermmap3',
  version="0.4.14",
  author="Michael Axiak, Rob Stacey, Prashant Sinha",
  author_email="prashant@ducic.ac.in",
  url="https://github.com/PrashntS/pybloomfiltermmap3",
  description="A Bloom filter (bloomfilter) for Python 3 built on mmap",
  license="MIT License",
  test_suite='tests.test_all',
  install_requires=[],
  ext_modules=ext_modules,
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: C',
    'Programming Language :: Cython',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  cmdclass={'build_ext': build_ext}
)
