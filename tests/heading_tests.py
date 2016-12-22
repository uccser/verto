import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.heading import *


class HeadingTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/heading/{}.txt'
        self.expected_file_path = 'tests/assets/heading/expected/{}.txt'

    def tearDown(self):
        self.md = None
