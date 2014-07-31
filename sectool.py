#!/usr/bin/env python3
from __future__ import print_function

import logging
logging.basicConfig(filename="sectool.log", filemode='a', level=logging.INFO)
import time
import datetime
from argh import arg, dispatch, set_default_command
from argparse import ArgumentParser, ArgumentError
from sys import exit, stderr
from sectool.plugin_loader import PluginLoader
from sectool.email_alert import Email

PLUGIN_LOADER = PluginLoader()
PLUGINS = PLUGIN_LOADER.plugins
CHECKERS = ['xss', 'sql', 'backup', 'file', 'exec']
FORMAT = ['html', 'markdown', 'json']
OUTPUT_FILE = "sectool-report-{0}-{1}.{2}"
FAILURE_CODE = 1


@arg('url', type=str, help="URL to test against.")
@arg('email', help="Email to send generated report to.")
@arg('--plugins', choices=PLUGINS, help="Plugins to use.", type=str, nargs='+')
@arg('--checkers', choices=CHECKERS, help="Checkers to use.", type=str,
     nargs='+')
@arg('--output', help="Output file name.", type=str)
@arg('--format', choices=FORMAT, help='Format type to use for output',
     type=str)
@arg('--auth', help="Credentials to use (auth%%password)", type=str)
@arg('--no_stdout', help="Show or hide console output from sectool",
     action='store_true')
def sectool(url, email, plugins=PLUGINS, checkers=CHECKERS[0:2], output=None,
            format=FORMAT[1], auth=None, no_stdout=False):
    """Run security plugins to check for vulnerabilities in web applications.
    This tool is designed to be integrated inside of a Continuous Integration
    pipeline.
    """

    if url is None or email is None:
        raise ArgumentError('url and email must both be specified')

    if auth is not None and len(auth.split("%")) > 2:
        raise ArgumentError("auth must have the format username%password")

    if output is None:
        output = generate_output_name(format, plugins)
    for plugin in plugins:
        instance = None
        try:
            instance = PLUGIN_LOADER.load_plugin(plugin)
        except NameError:
            msg = ("Could not find plugin with name {0}, "
                   "please enter name of valid plugin").format(plugin)
            print(msg, file=stderr)
            exit(FAILURE_CODE)

        t0 = time.time()
        try:
            file_loc = instance.run(url, checkers, output, auth)
        except (KeyboardInterrupt, SystemExit):
            try:
                instance.kill()
                exit()
            except ProcessLookupError:
                exit(1)
        t1 = time.time()
        time_taken = (t1 - t0) / 60
        logging.info("TIME TAKEN: {0:.2f} minutes".format(time_taken))
        send_email(url, email, file_loc, plugin, no_stdout, time_taken, format)


def generate_output_name(file_format, plugins):
    """Generate a filename with the format
        sectool-report-PLUGINS-DATE.FILEFORMAT.
    """
    date_frmt = "%y-%m-%d-%H%M"
    current_date = datetime.datetime.now().strftime(date_frmt)
    return OUTPUT_FILE.format('{0}{1}'.join(plugins), current_date, file_format)


def send_email(url, e_mail, file_loc, plugin, no_stdout, time_taken,
               output_format):
    """Send an e-mail with a report.
    """
    email_obj = Email(target_url=url, users_email_address=e_mail,
                      input_file=file_loc, plugin_name=plugin,
                      show_std_out=not no_stdout, duration=time_taken)
    email_obj.trigger_email_alert(output_format)


if __name__ == '__main__':
    parser = ArgumentParser()
    set_default_command(parser, sectool)
    dispatch(parser)
