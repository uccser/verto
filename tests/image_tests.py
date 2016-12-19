import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.image import *


class ImageTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/image/{}.txt'
        self.expected_file_path = 'tests/assets/image/expected/{}.txt'

    def tearDown(self):
        self.md = None
