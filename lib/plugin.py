"""
Plugin interface class. All plugins should inherit from here.
"""

from subprocess import Popen, PIPE


class ProcessException(Exception):
    """Exception raised if a process fails to execute or executes and returns
    a bad return code.
    """
    pass


class Plugin(object):
    """Represents the base methods a Plugin must implement.
    """
    def __init__(self, name):
        self.name = name

    def run(self, url, checks, output, output_format, auth):
        """Run the plugin with checks and output to output_format
        """
        return NotImplementedError("Method has not been implemented")

    def __exec_process__(self, cmd, good_ret=0):
        """Executes a process using Popen. Once the process has completed
        the return code is checked, if the return code is fine then stdout
        from the process is returned. If it is bad then a ProcessException is
        raised which has the return code, command used, and the stderr of the
        process. All text is normalised to UTF-8.
        """
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

        returncode = proc.returncode
        if returncode != good_ret:
            msg = "Proc returned {0} when command {1} was used. Message is {2}"
            msg = msg.format(returncode, ' '.join(cmd), str(stderr, 'utf-8'))
            raise ProcessException(msg)
        else:
            return str(stdout, 'utf-8')
