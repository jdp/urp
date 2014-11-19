% urp

**urp** is a command-line tool for building URLs, and for extracting and modifying their features.
It knows all about schemes, authentication, hosts, ports, paths, parameters, query strings, and fragments.

## Installation

urp is distributed through [PyPI][urp-pypi].
You can always get the latest with [pip][pip]:

    $ pip install urp

## Basic Recipes

Add to the path of a URL:

    $ urp -D bar http://domain.com/foo?baz=bux
    http://domain.com/foo/bar?baz=bux

Extract a value from a query parameter:

    $ urp -g q http://domain.com/search?q=urp%20is%20dope
    urp is dope

Add authorization to a protected resource:

    $ urp -U foo -W password http://protected.com
    http://foo:password@protected.com

Sign a request with an MD5 hex digest:

    $ url="http://api.com/resource?param=bux&app_id=foo"
    $ urp $url -Q signature=$(urp $url --sort-query -q | md5)
    http://api.com/resource?param=bux&app_id=foo&signature=f2d434f97779e6a31dbaf606b43064a5

<aside>
What do you use **urp** for? You should <a href="https://twitter.com/intent/tweet?screen_name=justinpoliey" data-related="justinpoliey">tell @justinpoliey</a>.
</aside>

## Documentation

**urp** is documented in its [manual page][urp-manual].

## Development

Development happens on the [GitHub project page][urp-repo].

---

Copyright &copy; 2014 [Justin Poliey](http://justinpoliey.com)

<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>

[pip]: https://pypi.python.org/pypi/pip
[urp-pypi]: https://pypi.python.org/pypi/urp
[urp-manual]: urp.1.html
[urp-repo]: https://github.com/jdp/urp