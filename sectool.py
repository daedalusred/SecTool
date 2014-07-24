#!/usr/bin/env python3

import time
import datetime
from argh import arg, dispatch, set_default_command
from argparse import ArgumentParser, ArgumentError
from lib.plugin_loader import PluginLoader
from emailAlert import Email

PLUGIN_LOADER = PluginLoader()
PLUGINS = PLUGIN_LOADER.plugins
CHECKERS = ['xss', 'sql', 'backup', 'file', 'exec']
FORMAT = ['json']
OUTPUT_FILE = "sectool-report-{0}-{1}.{2}"


@arg('url', type=str, help="URL to test against.")
@arg('email', help="Email to send generated report to.")
@arg('--plugins', choices=PLUGINS, help="Plugins to use.", type=str,
     nargs='+')
@arg('--checkers', choices=CHECKERS, help="Checkers to use.", type=str,
     nargs='+')
@arg('--output', help="Output file name.", type=str)
@arg('--format', choices=FORMAT, help='Format type to use for output',
     type=str)
@arg('--auth', help="Credentials to use (auth%password)", type=str)
def sectool(url, email, plugins=PLUGINS, checkers=CHECKERS[0:2], output=None,
            format=FORMAT[0], auth=None):
    """Run security plugins to check for vulnerabilities in web applications.
    This tool is designed to be integrated inside of a Continuous Integration
    pipeline.
    """

    if url is None or email is None:
        raise ArgumentError('url and email must both be specified')

    if auth is not None and len(auth.split("%")) > 2:
        print("auth must have the format username%password")

    if output is None:
        date_frmt = "%y-%m-%d-%H-%M"
        current_date = datetime.datetime.now().strftime(date_frmt)
        output = OUTPUT_FILE.format('{0}{1}'.join(plugins),
                                    current_date,
                                    format)
    for i in plugins:
        instance = PLUGIN_LOADER.load_plugin(i)
        t0 = time.time()
        file_loc = instance.run(url, checkers, output, format, auth)
        t1 = time.time()
        print("TIME TAKEN: ", (t1 - t0) / 60, " seconds")

        print(i)
        # Call e-mail with JSON filename?
        # url, json_filename, plugin
        send_email(url, email, file_loc, i)


def send_email(url, e_mail, file_loc, plugin):
    """Send an e-mail with a report.
    """
    email_obj = Email(targetUrl=url, usersEmailAddress=e_mail,
                      jsonOutputFileName=file_loc, pluginName=plugin)

    email_obj.triggerEmailAlert()


if __name__ == '__main__':
    parser = ArgumentParser()
    set_default_command(parser, sectool)
    dispatch(parser)
