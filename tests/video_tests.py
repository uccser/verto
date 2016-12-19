import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.video import *


class VideoTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/video/{}.txt'
        self.expected_file_path = 'tests/assets/video/expected/{}.txt'

    def tearDown(self):
        self.md = None
