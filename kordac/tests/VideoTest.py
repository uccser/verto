import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.VideoBlockProcessor import VideoBlockProcessor
from kordac.processors.errors.NoSourceLinkError import NoSourceLinkError
from kordac.processors.errors.NoVideoIdentifierError import NoVideoIdentifierError
from kordac.processors.errors.UnsupportedVideoPlayerError import UnsupportedVideoPlayerError
from kordac.tests.ProcessorTest import ProcessorTest


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

        self.assertListEqual([False, True, False, False, False, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

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
        test_string = self.read_test_file(self.processor_name, 'youtube_be_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_be_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_vimeo_link(self):
        test_string = self.read_test_file(self.processor_name, 'vimeo_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'vimeo_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_vimeo_player_link(self):
        test_string = self.read_test_file(self.processor_name, 'vimeo_player_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'vimeo_player_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_multiple_youtube_links(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_youtube_links.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, True, False, True, False, True, False, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'multiple_youtube_links_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_multiple_vimeo_links(self):
        test_string = self.read_test_file(self.processor_name, 'multiple_vimeo_links.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'multiple_vimeo_links_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_and_vimeo_links(self):
        test_string = self.read_test_file(self.processor_name, 'youtube_and_vimeo_links.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, True, False, True, False, True, False, True, True, False, True, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_and_vimeo_links_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_unsupported_video_type(self):
        test_string = self.read_test_file(self.processor_name, 'unsupported_video_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(UnsupportedVideoPlayerError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)

    def test_missing_identifier(self):
        test_string = self.read_test_file(self.processor_name, 'missing_identifier.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(NoVideoIdentifierError, lambda x: markdown.markdown(x, extensions=[self.kordac_extension]), test_string)


    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
