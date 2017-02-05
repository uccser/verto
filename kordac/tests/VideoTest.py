import markdown
from unittest.mock import Mock

from KordacExtension import KordacExtension
from processors.VideoBlockProcessor import VideoBlockProcessor
from tests.BaseTestCase import BaseTestCase

# NTS videos have different links
# need to test:
#   - vimeo
#   - youtu.be
#   - /embed/
#   - /watch/
# etc

class VideoTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'video'
        self.ext = Mock()
        self.ext.html_templates = {self.tag_name: BaseTestCase.loadHTMLTemplate(self, self.tag_name)}
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)

    def test_contains_no_video(self):
        test_string = self.read_test_file('contains_no_video')
        self.assertFalse(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[KordacExtension()])
        expected_file_string = self.read_expected_output_file('contains_no_video_expected')
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_youtube_video(self):
        test_string = self.read_test_file('contains_youtube_video')
        self.assertTrue(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[KordacExtension()])
        expected_file_string = self.read_expected_output_file('contains_youtube_video_expected')
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_vimeo_video(self):
        test_string = self.read_test_file('contains_vimeo_video')
        self.assertTrue(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[KordacExtension()])
        expected_file_string = self.read_expected_output_file('contains_vimeo_video_expected')
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_multiple_videos(self):
        test_string = self.read_test_file('contains_multiple_videos')
        self.assertTrue(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[KordacExtension()])
        expected_file_string = self.read_expected_output_file('contains_multiple_videos_expected')
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_another_tag(self):
        pass
