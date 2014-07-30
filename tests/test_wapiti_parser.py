
import unittest
from sectool.parsers.wapiti import Wapiti


class WapitiParserTest(unittest.TestCase):

    def test_markdown_generator(self):
        a = Wapiti()
        with open('tests/test_wapiti.json', 'r+') as f:
            a.parse_to_json(f.read())
