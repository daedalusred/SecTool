"""
Plugin interface class. All plugins should inherit from here.
"""

from subprocess import Popen, PIPE
import logging

import os
import signal


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
        self.pid = None

    def run(self, url, checks, output, auth):
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
        logging.info("Attempting to exec {0}".format(cmd[0]))

        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        self.pid = proc.pid
        stdout, stderr = proc.communicate()

        returncode = proc.returncode
        if returncode != good_ret:
            logging.error("Failed to execute {0} successfully".format(cmd[0]))
            msg = "Proc returned {0} when command {1} was used. Message is {2}"
            msg = msg.format(returncode, ' '.join(cmd), str(stderr, 'utf-8'))
            raise ProcessException(msg)
        else:
            logging.info("Successfully executed {0}".format(cmd[0]))
            return stdout.decode('utf-8')

    def kill(self):
        """Kill an executed process before it terminates normally.
        """
        if self.pid is not None:
            os.killpg(self.pid, signal.SIGTERM)
        else:
            raise Exception("PID is not set")
