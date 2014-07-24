"""Load Plugins from the plugins directory.
"""

from .plugins import wapiti
from os.path import splitext
from os import listdir

PLUGIN_LOC = "lib/plugins"
FILE_NAME_BLACKLIST = ["__init__.py", "__pycache__"]
FILE_EXT_BLACKLIST = [".swp"]


class PluginLoader(object):
    """Object that can load plugins and return constructed instances of a
    plugin.
    """

    def __init__(self):
        self.plugins = [splitext(x)[0] for x in listdir(PLUGIN_LOC)
                        if x not in FILE_NAME_BLACKLIST and
                        splitext(x)[1] not in FILE_EXT_BLACKLIST]

    def load_plugin(self, plugin_name):

        plugin_instance = eval("{0}.{1}".format(plugin_name,
                                                plugin_name.capitalize()))
        plugin_instance = plugin_instance(plugin_name)
        return plugin_instance
