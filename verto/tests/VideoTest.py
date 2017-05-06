import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.VideoBlockProcessor import VideoBlockProcessor
from verto.errors.NoSourceLinkError import NoSourceLinkError
from verto.errors.NoVideoIdentifierError import NoVideoIdentifierError
from verto.errors.UnsupportedVideoPlayerError import UnsupportedVideoPlayerError
from verto.tests.ProcessorTest import ProcessorTest


class VideoTest(ProcessorTest):
    '''The Video processor is similar to the a generic tag
    except that it requires custom validation for Video
    urls to extract identifiers and embedded properly.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a processor name and info for accessing testing
        assets.
        '''
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
        '''Tests that input that doesn't use the video processor tag is
        unchanged.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_no_video.md')
        blocks = self.to_blocks(test_string)

        self.assertFalse(all(VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks), msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_no_video_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_embed_link(self):
        '''Tests youtube embed links are properly embedded.
        '''
        test_string = self.read_test_file(self.processor_name, 'youtube_embed_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False, False, False, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_embed_link_expected.html', strip=True)

        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_watch_link(self):
        '''Tests that youtube links are converted into embedded form.
        '''
        test_string = self.read_test_file(self.processor_name, 'youtube_watch_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, False, False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_watch_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_be_link(self):
        '''Tests that short youtube links are embedded.
        '''
        test_string = self.read_test_file(self.processor_name, 'youtube_be_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_be_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_vimeo_link(self):
        '''Tests that vimeo links are converted into embedded form.
        '''
        test_string = self.read_test_file(self.processor_name, 'vimeo_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'vimeo_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_vimeo_player_link(self):
        '''Tests that the vimeo player links are embedded.
        '''
        test_string = self.read_test_file(self.processor_name, 'vimeo_player_link.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, False, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'vimeo_player_link_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_multiple_youtube_links(self):
        '''Tests output of multiple youtube links.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_youtube_links.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, True, False, True, False, True, False, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'multiple_youtube_links_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_multiple_vimeo_links(self):
        '''Tests output of multiple vimeo links.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_vimeo_links.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'multiple_vimeo_links_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_youtube_and_vimeo_links(self):
        '''Test that youtube links and vimeo links work together in the
        same document.
        '''
        test_string = self.read_test_file(self.processor_name, 'youtube_and_vimeo_links.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, True, False, True, False, True, False, True, True, False, True, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'youtube_and_vimeo_links_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)

    def test_unsupported_video_type(self):
        '''Tests that links to other websites result in an
        UnsupportedVideoPlayerError exception.
        '''
        test_string = self.read_test_file(self.processor_name, 'unsupported_video_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(UnsupportedVideoPlayerError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_identifier(self):
        '''Tests that a youtube link without an identifier will throw
        the NoVideoIdentifierError exception.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_identifier.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(NoVideoIdentifierError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_contains_multiple_videos(self):
        '''Tests output of multiple video links.
        '''
        test_string = self.read_test_file(self.processor_name, 'contains_multiple_videos.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, True, False, True, False, True, False], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_file_string = self.read_test_file(self.processor_name, 'contains_multiple_videos_expected.html', strip=True)
        self.assertEqual(converted_test_string, expected_file_string)
    #~
    # Doc Tests
    #~
    def test_doc_example_basic(self):
        '''A generic example of common usage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''A example showing how to override the html template.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [VideoBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
