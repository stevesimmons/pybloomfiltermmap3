import os
import sys

from setuptools import setup, Extension

try:
  from Cython.Distutils import build_ext
except ImportError:
  print("""Cannot find Cython!
  Cython is required to correctly build pyBloomFilter's C extensions.
  In most cases, running the following command should be sufficient:
    $ pip install Cython

  Exception: ImportError
  """)
  exit()

here = os.path.dirname(__file__)
# Get the long description from the README file
with open(os.path.join(here, 'README.markdown'), encoding='utf-8') as fp:
  long_description = fp.read()


ext_files = [
  'src/mmapbitarray.c',
  'src/bloomfilter.c',
  'src/md5.c',
  'src/primetester.c',
  'src/MurmurHash3.c',
  'src/pybloomfilter.pyx'
]

print("info: Building from Cython")

ext_modules = [
  Extension("pybloomfilter", ext_files, libraries=['crypto'])
]

if sys.version_info[0] < 3:
  raise SystemError('This Package is for Python Version 3 and above.')

setup(
  name='pybloomfiltermmap3',
  version="0.4.18",
  author="Michael Axiak, Rob Stacey, Prashant Sinha",
  author_email="prashant@noop.pw",
  url="https://github.com/prashnts/pybloomfiltermmap3",
  description="A Bloom filter (bloomfilter) for Python 3 built on mmap",
  long_description=long_description,
  long_description_content_type='text/markdown',
  license="MIT License",
  test_suite='tests.test_all',
  install_requires=['Cython'],
  ext_modules=ext_modules,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: C',
    'Programming Language :: Cython',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  cmdclass={'build_ext': build_ext}
)
