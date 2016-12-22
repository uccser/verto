import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.video import *


# NTS videos have different links
# need to test:
#   - vimeo
#   - youtu.be
#   - /embed/
#   - /watch/
# etc

class VideoTest(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(extensions=[CSFGExtension()])
        self.test_file_path = 'tests/assets/video/{}.txt'
        self.expected_file_path = 'tests/assets/video/expected/{}.txt'

    def test_match_false(self):
        test_string = open(self.test_file_path.format('fail_string')).read()
        self.assertFalse(VideoBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_match_true(self):
        test_string = open(self.test_file_path.format('basic')).read()
        self.assertTrue(VideoBlockProcessor(self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

    def test_parses(self):
        test_string = open(self.test_file_path.format('basic')).read()
        converted_test_string = markdown.markdown(test_string, extensions=[CSFGExtension()]) + '\n'
        expected_file_string = open(self.expected_file_path.format('basic_expected')).read()
        self.assertEqual(converted_test_string, expected_file_string)

    def tearDown(self):
        self.md = None
