.. Python BloomFilter documentation master file, created by
   sphinx-quickstart on Wed Mar 31 16:25:58 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python BloomFilter's documentation!
==============================================

`pybloomfiltermmap3` is a Python 3  fork of `pybloomfiltermmap` by `Michael Axiak (@axiak) <https://github.com/axiak>`_.

Bloom filter is a probablilistic data structure used to test whether an element
is a member of a set. The `wikipedia page <http://en.wikipedia.org/wiki/Bloom_filter>`_
has further information on their nature. This module implements a Bloom filter
in python that's fast and uses mmap files for better scalability.

Here's a quick example:

.. code-block:: python

    >>> from pybloomfilter import BloomFilter

    >>> bf = BloomFilter(10000000, 0.01, 'filter.bloom')
    >>> with open("/usr/share/dict/words") as f:
    >>>     for word in f:
    >>>         bf.add(word.rstrip())

    >>> print 'apple' in bf
    True

That wasn't so hard, was it? Now, there are a lot of other things
we can do. For instance, let's say we want to create a similar
filter with just a few pieces of fruit:

.. code:: python

    >>> fruitbf = bf.copy_template("fruit.bloom")
    >>> fruitbf.update(("apple", "banana", "orange", "pear"))

    >>> print(fruitbf.to_base64())
    "eJzt2k13ojAUBuA9f8WFyofF5TWChlTHaPzqrlqFCtj6gQi/frqZM2N7aq3Gis59d2ye85KTRbhk"
    "0lyu1NRmsQrgRda0I+wZCfXIaxuWv+jqDxA8vdaf21HIOSn1u6LRE0VL9Z/qghfbBmxZoHsqM3k8"
    "N5XyPAxH2p22TJJoqwU9Q0y0dNDYrOHBIa3BwuznapG+KZZq69JUG0zu1tqI5weJKdpGq7PNJ6tB"
    "GKmzcGWWy8o0FeNNYNZAQpSdJwajt7eRhJ2YM2NOkTnSsBOCGGKIIYbY2TA663GgWWyWfUwn3oIc"
    "fyLYxeQwiF07RqBg9NgHrG5ba3jba5yl4zS2LtEMMcQQQwwxmRiBhPGOJOywIPafYhUwqnTvZOfY"
    "Zu40HH/YxDexZojJwsx6ObDcT7D8vVOtJBxiAhD/AjMmjeF2Wnqd+5RrHdo4azPEzoANabiUhh0b"
    "xBBDDDHEENsf8twlrizswEjDhnTbzWazbGKpQ5k07E9Ox2iFvXBZ2D9B7DawyqLFu5lshhhiiGUK"
    "a4nUloa9yxkwR7XhgPPXYdhRIa77uDtnyvqaIXalGK02ufv3J36GmsnG4lquPnN9gJo1VNxqgYbt"
    "ji/EC8s1PWG5fuVizW4Jox6/3o9XxBBDDLFbwcg9v/AwjrPHtTRsX34O01mxLw37bhCTjJk0+PLK"
    "08HYd4MYYojdKmYnBfjsktEpySY2tGGZzWaIIfYDGB271Yaieaat/AaOkNKb"

Reference
------------

All of the reference information is available below:

.. toctree::
   :maxdepth: 2

   ref



Why pybloomfilter
---------------------

As already mentioned, there are a couple reasons to use this module:

 * It natively uses `mmaped files <http://en.wikipedia.org/wiki/Mmap>`_.
 * It natively does the set things you want a Bloom filter to do.
 * It is Fast (see Benchmarks by Michael Axiak).


Install
---------------------

Please have `Cython` installed. Please note that this version is for Python 3.
In case you are using Python 2, please see https://github.com/axiak/pybloomfiltermmap.

To install::

    $ pip install cython
    $ pip install pybloomfiltermmap3

to build and install the module.

Develop
-----------------------

To develop you will need Cython. The setup.py script should automatically
build from Cython source if the Cython module is available.
