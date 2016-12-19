import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.interactive import *


class InteractiveTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/interactive/{}.txt'
        self.expected_file_path = 'tests/assets/interactive/expected/{}.txt'

    def tearDown(self):
        self.md = None
