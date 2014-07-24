#!/usr/bin/env python3

import datetime
from argh import arg, dispatch, set_default_command
from argparse import ArgumentParser, ArgumentError

PLUGINS = ['wapiti']
CHECKERS = ['xss', 'sql']
FORMAT = ['json']
OUTPUT_FILE = "sectool-report-{0}-{1}"


@arg('url', type=str, help="URL to test against.")
@arg('email', help="Email to send generated report to.")
@arg('--plugins', choices=PLUGINS, help="Plugins to use.", type=str,
     nargs='+')
@arg('--checkers', choices=CHECKERS, help="Checkers to use.", type=str,
     nargs='+')
@arg('--output', help="Output file name.", type=str)
@arg('--format', choices=FORMAT, help='Format type to use for output',
     type=str)
def sectool(url, email, plugins=PLUGINS, checkers=CHECKERS, output=None,
            format=FORMAT):
    """Run security plugins to check for vulnerabilities in web applications.
    This tool is designed to be integrated inside of a Continuous Integration
    pipeline.
    """
    if url is None or email is None:
        raise ArgumentError('url and email must both be specified')
    if output is None:
        output = OUTPUT_FILE.format('$'.join(plugins),
                                    datetime.datetime.now())
    print(output)

if __name__ == '__main__':
    parser = ArgumentParser()
    set_default_command(parser, sectool)
    dispatch(parser)
