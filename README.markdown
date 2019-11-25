# pybloomfiltermmap3

`pybloomfiltermmap3` is a `Python 3` compatible fork of `pybloomfiltermmap` by @axiak.

The goal of `pybloomfiltermmap3` is simple: to provide a fast, simple, scalable, correct library for Bloom Filters in Python.

[![Build Status](https://travis-ci.org/PrashntS/pybloomfiltermmap3.svg?branch=master)](https://travis-ci.org/PrashntS/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/v/pybloomfiltermmap3.svg)](https://pypi.python.org/pypi/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/dw/pybloomfiltermmap3.svg)](https://pypi.python.org/pypi/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/pyversions/pybloomfiltermmap3.svg)](https://pypi.python.org/pypi/pybloomfiltermmap3)


## Quickstart

After you install, the interface to use is a cross between a file
interface and an ste interface. As an example:
```python
    >>> import pybloomfilter
    >>> fruit = pybloomfilter.BloomFilter(100000, 0.1, '/tmp/words.bloom')
    >>> fruit.update(('apple', 'pear', 'orange', 'apple'))
    >>> len(fruit)
    3
    >>> 'mike' in fruit
    False
    >>> 'apple' in fruit
    True
```

To create an in-memory filter, simply omit the file location:
```python
    >>> cakes = pybloomfilter.BloomFilter(10000, 0.1)
```
*Caveat*: It is currently not possible to persist this filter later.


## Docs

Follow the *official* docs for `pybloomfiltermmap` at: http://axiak.github.io/pybloomfiltermmap/


## Install

Please note that this version is **specifically** meant for Python 3. In case you need Python 2, please see https://github.com/axiak/pybloomfiltermmap.

To install:

```shell
    $ pip install pybloomfiltermmap3
```

and you should be set.

## History and Future

`pybloomfiltermmap` is an excellent `bloomfiler` implementation for `Python 2` by @axiak and contributors.
I (@prashnts) made tiny changes to add support for `Python 3` sometime in 2016 as `pybloomfiltermmap3` on
`PyPI`. Since then through the help of contributors there has been incremental improvements and bugfixes
while maintaining the API in `v0.4.x`. Since Nov. 2019, @mizvyt joined in this project and has made tons
of fixes, and added support for Read-Only bloomfilters (check #12).

We're moving the new changes to `v0.5.x` and onwards. The goal would be to reach stability as well as add
few more APIs to expand upon the use cases. While this won't be guaranteed to not remove or change the
interface, the transition from `v0.4.x` should be quick one liners. Please open an issue if we broke your
build!

Suggestions, bug reports, and/or patches are welcome!


## License

See the LICENSE file. It's under the MIT License.


## Contributions and development

When contributing, you should set up an appropriate Python 3 environment and install the dependencies listed in `requirements-dev.txt`.
This package depends on generation of `pybloomfilter.c` and requires Cython to be packaged.

