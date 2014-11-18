===
Urp
===

**urp** parses URLs.
It's a command-line tool that enables users to extract and modify their features.
It knows all about
schemes,
authentication,
hosts,
ports,
paths,
parameters,
query strings,
and
fragments.

Installation
------------

Install from PyPI::

$ pip install urp

Install from git checkout::

$ git clone https://github.com/jdp/urp.git
$ cd urp
$ python setup.py install

Basic Usage
-----------

**urp** takes URLs as input,
and outputs URLs or features of URLs depending on its options.
It takes URLs specified as arguments and newline-delimited URLs from standard input.

::

  $ urp -s https://google.com
  https
  $ echo 'https://google.com' | urp -s
  https
  $ urp -D /search -Q q=urp 'https://google.com'
  https://google.com/search?q=urp

Documentation
-------------

The **urp** tool has a fully documented `manual page <http://jdp.github.com/urp/man/urp.1.html>`_.
