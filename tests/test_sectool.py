
import unittest
import lib.plugin_loader as plugin_loader
from tests.plugins.test import Test


class LoaderTests(unittest.TestCase):

    def setUp(cls):
        plugin_loader.PLUGIN_LOC = "tests/plugins"
        cls.loader_inst = plugin_loader.PluginLoader()
        plugin_loader.test = __import__("tests").plugins.test

    def test_PluginLoader_hasrighttype(self):
        """Test that we get the right type of object returned by the loader.
        """
        plugin_instance = self.loader_inst.load_plugin("test")
        self.assertIsInstance(plugin_instance, Test)

    def test_PluginLoader_hasrightname(self):
        """Test that we get the right name attr returned by the loader.
        """
        plugin_instance = self.loader_inst.load_plugin("test")
        self.assertEqual("test", plugin_instance.name)

    def test_PluginLoader_canexec_success(self):
        """Test that we can exec a process with successfull execution.
        """
        plugin_instance = self.loader_inst.load_plugin("test")
        try:
            stdout = plugin_instance.__exec_process__(["ls"])
            self.assertGreater(len(stdout), 0)
        except Exception:
            self.fail("Failed to run successfully")

    def test_PluginLoader_canexec_failure(self):
        """Test that we can exec a process and handle failed execution.
        """
        plugin_instance = self.loader_inst.load_plugin("test")
        try:
            plugin_instance.__exec_process__(["foooooo"])
            self.fail("Failed to fail")
        except Exception:
            self.assertEqual(0, 0)
