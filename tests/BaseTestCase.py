import unittest
import json
import markdown
from kordac.KordacExtension import KordacExtension
from markdown.extensions import Extension

class BaseTestCase(unittest.TestCase):
    """A base test class for individual test classes"""

    def __init__(self, *args, **kwargs):
        """Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        """
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.test_file_path = 'tests/assets/{tag_name}/{filename}.md'
        self.expected_output_file_path = 'tests/assets/{tag_name}/{filename}.html'
        self.maxDiff = 640  # Set to None for full output of all test failures
        # self.maxDiff = None

    def read_test_file(self, filename):
        """Returns a string for a given file

        This function reads a file from a given filename in UTF-8 encoding.
        """
        file_path = self.test_file_path.format(tag_name=self.tag_name, filename=filename)
        file_object = open(file_path, encoding="utf-8")
        return file_object.read()

    def read_expected_output_file(self, filename):
        """Returns a string for a given file

        This function reads a file from a given filename in UTF-8 encoding.
        """
        file_path = self.expected_output_file_path.format(tag_name=self.tag_name, filename=filename)
        file_object = open(file_path, encoding="utf-8")
        return file_object.read()

    def loadHTMLTemplate(self, template):
        return open('kordac/html-templates/' + template + '.html').read()

    def loadTagPatterns(self):
        pattern_data = open('kordac/regex-list.json').read()
        return json.loads(pattern_data)

    def setUp(self):
        self.kordac_extension = KordacExtension([self.tag_name], {})
        self.md = markdown.Markdown(extensions=[self.kordac_extension])

    def tearDown(self):
        self.md = None
