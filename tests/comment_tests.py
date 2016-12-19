import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.comment import *


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/comment/{}.txt'
        self.expected_file_path = 'tests/assets/comment/expected/{}.txt'

    def tearDown(self):
        self.md = None
