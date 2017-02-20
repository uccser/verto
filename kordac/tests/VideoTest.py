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
        self.ext.jinja_templates = {
                self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name),
                'video-youtube': ProcessorTest.loadJinjaTemplate(self, 'video-youtube'),
                'video-vimeo': ProcessorTest.loadJinjaTemplate(self, 'video-vimeo')
                }
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

    def test_contains_no_video(self):
        test_string = self.read_test_file(self.processor_name, 'contains_no_video.md')
        blocks = self.to_blocks(test_string)

        self.assertFalse(all(VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_no_video_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_embed_link(self):
        test_string = self.read_test_file(self.processor_name, 'youtube_embed_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_embed_link_expected.html', strip=True)

        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_watch_link(self):
        test_string = self.read_test_file(self.processor_name, 'youtube_watch_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, False, False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_watch_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

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

