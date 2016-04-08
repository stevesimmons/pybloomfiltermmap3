# pybloomfiltermmap3

`pybloomfiltermmap3` is a `Python 3` compatible fork of `pybloomfiltermmap` by @axiak.

The goal of `pybloomfiltermmap3` is simple: to provide a fast, simple, scalable, correct library for Bloom Filters in Python.

[![Build Status](https://travis-ci.org/PrashntS/pybloomfiltermmap3.svg?branch=master)](https://travis-ci.org/PrashntS/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/v/pybloomfiltermmap3.svg)](https://pypi.python.org/pypi/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/dw/pybloomfiltermmap3.svg)](https://pypi.python.org/pypi/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/pyversions/pybloomfiltermmap3.svg)](https://pypi.python.org/pypi/pybloomfiltermmap3)


## Quickstart

After you install, the interface to use is a cross between a file
interface and a ste interface. As an example:
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

## Docs

Follow the *official* docs for `pybloomfiltermmap`. http://axiak.github.io/pybloomfiltermmap/

## Install

Please have `Cython` installed. Please note that this version is **specifically** meant for Python 3. In case you need Python 2, please see https://github.com/axiak/pybloomfiltermmap.

To install:

```shell
    $ pip install cython
    $ pip install pybloomfiltermmap3
```

and you should be set.


## License

See the LICENSE file. It's under the MIT License.

