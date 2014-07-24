"""Plugin that wraps wapiti.
"""

from ..plugin import Plugin


class Wapiti(Plugin):
    """Wapiti is a web app scanning tool that searches for numerous
    vulnerabilities.
    """

    def __init__(self, name):
        super().__init__(name)

    def run(self, url, checkers, output, output_format, auth):
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
            self.__exec_process__(cmd)
            return output
        except Exception:
            raise
