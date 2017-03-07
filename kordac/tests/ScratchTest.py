import markdown
from unittest.mock import Mock
from collections import defaultdict

from kordac.KordacExtension import KordacExtension
from kordac.processors.ScratchTreeprocessor import ScratchTreeprocessor, ScratchImageMetaData
from kordac.tests.ProcessorTest import ProcessorTest

class ScratchTest(ProcessorTest):
    def __init__(self, *args, **kwargs):
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'scratch'

    #~
    # Doc Tests
    #~
    def test_doc_example_basic(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        # Should really test result a better way
        actual = self.kordac_extension.required_files['scratch_images']
        expected = {
                        ScratchImageMetaData(
                            hash='a0f8fcad796864abfacac8bda6e0719813833fd1fca348700abbd040557c1576',
                            text='when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees'
                        ),
                    }
        self.assertSetEqual(actual, expected)

    def test_doc_example_override_html(self):
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        actual = kordac_extension.required_files['scratch_images']
        expected = {
                        ScratchImageMetaData(
                            hash='a3b77ed3c3fa57e43c830e338dc39d292c7def676e0e8f7545972b7da20275da',
                            text='when flag clicked\nsay [Hi]'
                        ),
                    }
        self.assertSetEqual(actual, expected)

    #~
    # Other Tests
    #~
    def test_example_separate_blocks(self):
        test_string = self.read_test_file(self.processor_name, 'example_separate_blocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_separate_blocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        # Should really test result a better way
        actual = self.kordac_extension.required_files['scratch_images']
        expected = {
                        ScratchImageMetaData(
                            hash='8e8a2129c3cecf32101248439961735fc1d45793fadc56e2575673f63d42b9fb',
                            text='when flag clicked\nclear\nforever\npen down\n\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\n\nmove (foo) steps\nturn ccw (9) degrees'
                        ),
                    }
        self.assertSetEqual(actual, expected)


    def test_example_multiple_codeblocks(self):
        test_string = self.read_test_file(self.processor_name, 'example_multiple_codeblocks.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_multiple_codeblocks_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        # Should really test result a better way
        actual = self.kordac_extension.required_files['scratch_images']
        expected = {
                        ScratchImageMetaData(
                            hash='a3b77ed3c3fa57e43c830e338dc39d292c7def676e0e8f7545972b7da20275da',
                            text='when flag clicked\nsay [Hi]'
                        ),
                        ScratchImageMetaData(
                            hash='cd6d9a0d464bb8f5eec1e6fc9a4e33378a64ebfce7c6198794ead614962f38e5',
                            text='when flag clicked\nsay [Hi]\nmove (foo) steps\nturn ccw (9) degrees'
                        ),
                        ScratchImageMetaData(
                            hash='8e8a2129c3cecf32101248439961735fc1d45793fadc56e2575673f63d42b9fb',
                            text='when flag clicked\nclear\nforever\npen down\n\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\n\nmove (foo) steps\nturn ccw (9) degrees'
                        ),
                    }
        self.assertSetEqual(actual, expected)

    def test_example_other_code(self):
        test_string = self.read_test_file(self.processor_name, 'example_other_code.md')

        converted_test_string = markdown.markdown(test_string, extensions=['markdown.extensions.fenced_code', self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_other_code_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        # Should really test result a better way
        actual = self.kordac_extension.required_files['scratch_images']
        expected = {
                        ScratchImageMetaData(
                            hash='a0f8fcad796864abfacac8bda6e0719813833fd1fca348700abbd040557c1576',
                            text='when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees'
                        ),
                    }
        self.assertSetEqual(actual, expected)
