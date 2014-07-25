"""
Plugin for Garmr.
"""
from ..plugin import Plugin


class Garmr(Plugin):

    def __init__(self, name):
        super().__init__(name)

    def run(self, url, checks, output, output_format, auth):
        """Run Garmr. Garmr doesn't use the checks, output_format or auth arguments.
        """
        try:
            cmd = ['garmr', '-u', url, '-o', output, '-r',
                   output_format]
            print(cmd)
            self.__exec_process__(cmd)
            return output
        except Exception:
            raise
