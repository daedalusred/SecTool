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
        super().__init__(name)

    def run(self, url, checkers, output, output_format, auth):
        """Wapiti uses all of the arguments passed but auth is optional.
        """
        logging.info("Loading Plugin Wapiti")

        if not isinstance(checkers, list):
            checkers = [checkers]

        if 'xss' in checkers:
            checkers.append('permanentxss')

        checkers.extend(['nikto', 'htaccess', 'crlf'])

        try:
            checker_liststr = ','.join(checkers)
            cmd = ['wapiti', url, '-m', '-all,' + checker_liststr, '--format',
                   output_format, '-o', output]

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
