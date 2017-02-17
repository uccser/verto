import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.VideoBlockProcessor import VideoBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest

# NTS videos have different links
# need to test:
#   - vimeo
#   - youtu.be
#   - /embed/
#   - /watch/
# etc

class VideoTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'video'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_patterns = ProcessorTest.loadProcessorPatterns(self)

    def test_contains_no_video(self):
        test_string = self.read_test_file(self.processor_name, 'contains_no_video.md')
        self.assertFalse(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_no_video_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_youtube_video(self):
        test_string = self.read_test_file(self.processor_name, 'contains_youtube_video.md')
        self.assertTrue(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_youtube_video_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_vimeo_video(self):
        test_string = self.read_test_file(self.processor_name, 'contains_vimeo_video.md')
        self.assertTrue(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_vimeo_video_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_multiple_videos(self):
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_videos.md')
        self.assertTrue(VideoBlockProcessor(self.ext, self.md.parser).test(None, test_string), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_multiple_videos_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_contains_another_processor(self):
        pass
