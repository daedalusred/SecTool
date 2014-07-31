"""Plugin that wraps wapiti for use in sectool.
"""

from ..plugin import Plugin
import logging


class Wapiti(Plugin):
    """Wapiti is a web app scanning tool that searches for numerous
    vulnerabilities, this plugin enables running of wapiti with a default or
    user selected arguments.
    """

    def __init__(self, name):
        super(Wapiti, self).__init__(name)

    def run(self, url, checkers, output, auth):
        """Wapiti uses all of the arguments passed but auth is optional.
        """
        logging.info("Loading Plugin Wapiti")

        if not isinstance(checkers, list):
            checkers = [checkers]

        if 'xss' in checkers:
            checkers.append('permanentxss')

        checkers.extend(['htaccess', 'crlf'])  # nikto is causing errors
        logging.info("Using checkers {0}".format(' ,'.join(checkers)))

        try:
            checker_liststr = ','.join(checkers)
            cmd = ['wapiti', url, '-m', '-all,' + checker_liststr, '--format',
                   'json', '-o', output, '--verify-ssl', '0']

            if auth is not None:
                cmd.extend(['--auth', auth])

            logging.info("Generating command {0}".format(' '.join(cmd)))
            self.__exec_process__(cmd)
            logging.info("Executed and received {0} on stdout".format(output))

            return output

        except Exception as e:
            logging_str = "Unsuccessfully executed command with error {0}"
            logging_str = logging_str.format(e)
            logging.error(logging_str)
            raise
