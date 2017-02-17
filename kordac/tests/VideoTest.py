import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.VideoBlockProcessor import VideoBlockProcessor
from kordac.tests.BaseTestCase import BaseTestCase

# NTS videos have different links
# need to test:
#   - vimeo
#   - youtu.be
#   - /embed/
#   - /watch/
# etc

class VideoTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'video'
        self.ext = Mock()
        self.ext.jinja_templates = {
                self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name),
                'video-youtube': BaseTestCase.loadJinjaTemplate(self, 'video-youtube'),
                'video-vimeo': BaseTestCase.loadJinjaTemplate(self, 'video-vimeo')
                }
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)

    def test_contains_no_video(self):
        test_string = self.read_test_file('contains_no_video')
        blocks = self.to_blocks(test_string)

        self.assertFalse(all(VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) == False for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_expected_output_file('contains_no_video_expected')
        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_embed_link(self):
        test_string = self.read_test_file('youtube_embed_link')
        blocks = self.to_blocks(test_string)

        # assert equal for two lists of T/F values to make sure only one match found
        pass

    def tests_youtube_watch_link(self):
        pass

    def test_youtube_be_link(self):
        pass

    def test_vimeo_link(self):
        pass

    def test_multiple_youtube_links(self):
        # assert equal for two lists of T/F values to make sure the expected number of links are found
        pass

    def test_multiple_vimeo_links(self):
        pass

    def test_youtube_and_vimeo_links(self):
        pass

