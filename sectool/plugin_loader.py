"""Load Plugins from the plugins directory.
"""

from .plugins import wapiti
assert wapiti  # Silence unused import warnings
from os.path import splitext
from os import listdir
import logging
import errno

PLUGIN_LOC = "sectool/plugins"  # Location of Plugin Dir.
FILE_NAME_BLACKLIST = ["__init__.py", "__pycache__"]  # Ignore these files
FILE_EXT_BLACKLIST = [".swp"]   # Ignore files with this extension


class PluginLoader(object):
    """An object that constructs a Plugin and returns an instance of it.
    """
    def __init__(self):
        try:
            items = listdir(PLUGIN_LOC)
            self.plugins = [splitext(x)[0] for x in items
                            if x not in FILE_NAME_BLACKLIST and
                            splitext(x)[1] not in FILE_EXT_BLACKLIST]
            logging.info("Found plugins {0}".format(' '.join(self.plugins)))

        except (OSError, IOError) as e:
            if e.errno == errno.ENOENT:
                msg = "Failed to listdir for plugin {0} with {1}"
                msg = msg.format(PLUGIN_LOC, e.errno)
                logging.error(msg)
            else:
                msg = "Failed to listdir for plugin {0} with {1}"
                msg = msg.format(PLUGIN_LOC, e.errno)
                logging.error(msg)
            raise

    def load_plugin(self, plugin_name):
        """Load a plugin from the plugins directory with the name set in
        plugin_name. If an instance can't be found raise that exception.
        """
        try:
            logging.info("Getting plugin {0}".format(plugin_name))
            plugin_instance = eval("{0}.{1}".format(plugin_name,
                                                    plugin_name.capitalize()))
            plugin_instance = plugin_instance(plugin_name)
            return plugin_instance
        except NameError:
            logging.error("failed getting plugin {0}".format(plugin_name))
            raise
