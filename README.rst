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

Printing URL Features
---------------------

If any of these options are specified,
**urp** will abandon its default behavior of printing full URLs
and instead print the features specified.

-s, --print-scheme    Print scheme.
-u, --print-username  Print username.
-w, --print-password  Print password.
-o, --print-hostname  Print hostname.
-p, --print-port      Print port.
-a, --print-authority
                    Print authority.
                    The authority is comprised of the `username`,
                    `password`,
                    `hostname`,
                    and
                    `port`.
-d, --print-path      Print path.
--print-params        Print params.
-q, --print-query     Print query string.
--print-query-names   Print query parameter names.
--print-query-values  Print query parameter values.
-f, --print-fragment  Print fragment.
-g QUERY, --print-query-value QUERY
                    Print value of query parameter.

Modifying URLs
--------------

Modifying features of URLs will cause the changes to be reflected in the output,
both through the printing options and through default behavior.

-S SCHEME, --scheme SCHEME
                    Set scheme to `SCHEME`.
-U USERNAME, --username USERNAME
                    Set username to `USERNAME`.
-W PASSWORD, --password PASSWORD
                    Set password to `PASSWORD`.
-O HOSTNAME, --hostname HOSTNAME
                    Set hostname to `HOSTNAME`.
-P PORT, --port PORT  Set port to `PORT`.
-D PATH, --path PATH  Set or append path as `PATH`.
                    If `PATH` begins with a ``/`` then the path is replaced.
                    Otherwise it is appended to the existing path.
--params PARAMS       Set params to `PARAMS`.
--query QUERY         Set query to `QUERY`.
-Q PAIR, --append-query PAIR
                    Append query parameter. `PAIR` should have the format ``NAME=VALUE``.
-F FRAGMENT, --fragment FRAGMENT
                    Set fragment to `FRAGMENT`.

Altering Behavior
-----------------

By default,
**urp** outputs URL-encoded fields where necessary
and preserves the order of query parameters.

--no-url-encoding     Disable URL encoding in output.
--no-query-params     Disable query parameter parsing.
                    **urp** will not try to parse `NAME=VALUE` pairs from queries.
--sort-query          Sort query parameters by name in output.
-x QUERY, --ignore-query QUERY
                    Ignore query parameter.

Each URL processed emits a `record`,
consisting of multiple `fields`.
By default,
records are separated with newlines
and fields are separated with spaces.
To change the record separator,
set the ``RS`` environment variable.
To change the field separator,
set the ``OFS`` environment variable.
