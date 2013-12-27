#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import itertools
import os
import sys
try:
    from urllib import quote_plus, urlencode
    from urlparse import parse_qsl, urlparse, urlunparse
except ImportError:
    from urllib.parse import parse_qsl, quote_plus, urlencode, urlparse, urlunparse

ERR_INVALID_PAIR = 3


def parse(args, data):
    url = urlparse(data)
    query = url.query
    if not args.no_query_params:
        query = parse_qsl(url.query)
    return url, query


def build_authority(username, password, hostname, port):
    netloc = hostname
    if username or password:
        auth = username + ':' + password
        netloc = auth + '@' + netloc
    if port:
        netloc += ':' + port
    return netloc


def process(args, url, query):
    scheme = args.scheme or url.scheme

    username = args.username or (url.username or '')

    password = args.password or (url.password or '')

    hostname = args.hostname or (url.hostname or '')

    port = str(args.port or (url.port or ''))

    params = args.params or url.params

    fragment = args.fragment or url.fragment

    authority = build_authority(username, password, hostname, port)

    path = url.path
    if args.path:
        if args.path.startswith('/'):
            path = args.path
        else:
            path = os.path.join(url.path, args.path)
        path = os.path.normpath(path)

    if args.no_query_params:
        if args.query:
            query = args.query
        if args.queries:
            query += ''.join(args.queries)
        if args.no_url_encoding:
            encoded_query = query
        else:
            encoded_query = quote_plus(query)
    else:
        if args.query:
            query = parse_qsl(args.query)
        if args.queries:
            query.extend(p.split('=', 2) for p in args.queries)
        query = [(q, v) for q, v in query if q not in args.ignored_queries]
        if args.sort_query:
            query = sorted(query, key=lambda p: p[0])
        if args.no_url_encoding:
            encoded_query = '&'.join('='.join(p) for p in query)
        else:
            encoded_query = urlencode(query)

    suppress_default = False

    if args.print_scheme:
        suppress_default = True
        yield scheme

    if args.print_username:
        suppress_default = True
        yield username

    if args.print_password:
        suppress_default = True
        yield password

    if args.print_hostname:
        suppress_default = True
        yield hostname

    if args.print_port:
        suppress_default = True
        yield port

    if args.print_authority:
        suppress_default = True
        yield authority

    if args.print_path:
        suppress_default = True
        yield path

    if args.print_params:
        suppress_default = True
        yield params

    if args.print_query:
        suppress_default = True
        yield encoded_query

    if args.query_value and not args.no_query_params:
        suppress_default = True
        # Would be nice to make `query_map` a defaultdict, but that would
        # restrict this program to newer Python versions.
        query_map = {}
        for q, v in query:
            if q not in query_map:
                query_map[q] = []
            query_map[q].append(v)
        for q in args.query_value:
            for v in query_map.get(q, ['']):
                yield v

    if args.print_query_names and not args.no_query_params:
        suppress_default = True
        for q in query:
            yield q[0]

    if args.print_query_values and not args.no_query_params:
        suppress_default = True
        for q in query:
            yield q[1]

    if args.print_fragment:
        suppress_default = True
        yield fragment

    if not suppress_default:
        yield urlunparse((scheme, authority, path, params, encoded_query, fragment))


def main():
    ap = argparse.ArgumentParser(description='extract and modify URL features')
    # URL-printing options
    ap.add_argument('-s', '--print-scheme', action='store_true', dest='print_scheme', help="print scheme")
    ap.add_argument('-u', '--print-username', action='store_true', dest='print_username', help="print username")
    ap.add_argument('-w', '--print-password', action='store_true', dest='print_password', help="print password")
    ap.add_argument('-o', '--print-hostname', action='store_true', dest='print_hostname', help="print hostname")
    ap.add_argument('-p', '--print-port', action='store_true', dest='print_port', help="print port")
    ap.add_argument('-a', '--print-authority', action='store_true', dest='print_authority', help="print authority")
    ap.add_argument('-d', '--print-path', action='store_true', dest='print_path', help="print path")
    ap.add_argument(      '--print-params', action='store_true', dest='print_params', help="print params")
    ap.add_argument('-q', '--print-query', action='store_true', dest='print_query', help="print query string")
    ap.add_argument(      '--print-query-names', action='store_true', dest='print_query_names', help="print only query parameter names")
    ap.add_argument(      '--print-query-values', action='store_true', dest='print_query_values', help="print only query parameter values")
    ap.add_argument('-f', '--print-fragment', action='store_true', dest='print_fragment', help="print fragment")
    ap.add_argument('-g', '--print-query-value', action='append', metavar='QUERY', dest='query_value', help="print value of query parameter")
    # URL-mutating options
    ap.add_argument('-S', '--scheme', action='store', dest='scheme', help="set scheme")
    ap.add_argument('-U', '--username', action='store', dest='username', help="set username")
    ap.add_argument('-W', '--password', action='store', dest='password', help="set password")
    ap.add_argument('-O', '--hostname', action='store', dest='hostname', help="set hostname")
    ap.add_argument('-P', '--port', action='store', dest='port', help="set port")
    ap.add_argument('-D', '--path', action='store', dest='path', help="set or append path")
    ap.add_argument(      '--params', action='store', dest='params', help="set params")
    ap.add_argument(      '--query', action='store', dest='query', help="set query")
    ap.add_argument('-Q', '--append-query', metavar='NAME=VALUE', action='append', dest='queries', default=[], help="append query parameter")
    ap.add_argument('-F', '--fragment', action='store', dest='fragment', help="set fragment")
    # Behavior-modifying options
    ap.add_argument(      '--no-url-encoding', action='store_true', help="disable URL encoding")
    ap.add_argument(      '--no-query-params', action='store_true', help="disable query parameter parsing")
    ap.add_argument(      '--sort-query', action='store_true', help="sort printed query parameters by name")
    ap.add_argument('-x', '--ignore-query', action='append', dest='ignored_queries', metavar='QUERY', default=[], help="ignore query parameter")
    ap.add_argument(      '--version', action='version', version='%(prog)s 0.1.1')
    # Positional arguments
    ap.add_argument('urls', nargs='*', metavar='URL')
    args = ap.parse_args()

    for pair in args.queries:
        if '=' not in pair:
            sys.stderr.write("invalid name=value pair: {}\n".format(pair))
            sys.exit(ERR_INVALID_PAIR)

    # Use the field and record separators from the environment
    ofs = os.environ.get('OFS', ' ')
    rs = os.environ.get('RS', '\n')

    inputs = []
    if not sys.stdin.isatty():
        inputs.append(sys.stdin)
    inputs.append(args.urls)
    for line in itertools.chain(*inputs):
        url, query = parse(args, line.strip())
        output = process(args, url, query)
        sys.stdout.write(ofs.join(output))
        sys.stdout.write(rs)


if __name__ == '__main__':
    main()
