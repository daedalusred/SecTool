#!/usr/bin/env python3

import argh
import datetime
from argh import arg

PLUGIN_LIST = ['wapiti']
DEFAULT_CHECKERS = ['xss', 'sql']
DEFAULT_FORMAT = 'json'
DEFAULT_OUTPUT_FILENAME = "sectool-report-{0}-{1}"


@arg('u', nargs=1, type=str, help="URL to test against.")
@arg('e', nargs=1, type=str, help="Email to send generated report to.")
@arg('--plugins', choices=PLUGIN_LIST, help="Plugins to use.")
@arg('--checkers', choices=DEFAULT_CHECKERS, help="Checkers to use.")
@arg('--output', help="Output file name.")
def sectool(u, e, plugins=PLUGIN_LIST, checkers=DEFAULT_CHECKERS, output=None):
    if not any([u, e]):
        print("Failed to set arg")
    if output is None:
        output = DEFAULT_OUTPUT_FILENAME.format('$'.join(plugins),
                                                datetime.datetime.now())

    print(u, e, plugins, checkers, output)


if __name__ == '__main__':
    argh.dispatch_command(sectool)
