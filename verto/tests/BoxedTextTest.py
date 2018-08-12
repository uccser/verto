import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.GenericContainerBlockProcessor import GenericContainerBlockProcessor
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.tests.ProcessorTest import ProcessorTest


class BoxedTextTest(ProcessorTest):
    '''The BoxedText processor inherits from the generic container.
    The tests contained here test that arguments and the output
    (html-template) work as expected.
    '''

    def __init__(self, *args, **kwargs):
        '''Sets up a generic container to test that the matches are
        occuring appropriately.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'boxed-text'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.block_processor = GenericContainerBlockProcessor(self.processor_name, self.ext, Mock())

    def test_no_boxed_text(self):
        '''Tests that the text containing the processor name is not matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'no_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False, False, False, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'no_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_single_boxed_text(self):
        '''Tests that the most generic case of a single match is found with generic content contained within.
        '''
        test_string = self.read_test_file(self.processor_name, 'single_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'single_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_boxed_text_type(self):
        '''Tests that, when specified, type is added to class
        '''
        test_string = self.read_test_file(self.processor_name, 'boxed_text_type.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'boxed_text_type_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_indented_boxed_text(self):
        '''Tests that the indented argument works as appropriate.
        '''
        test_string = self.read_test_file(self.processor_name, 'indented_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'indented_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_indented_and_type_boxed_text(self):
        '''Tests that the indented and type arguments work as expected when both used.
        '''
        test_string = self.read_test_file(self.processor_name, 'indented_type_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'indented_type_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_boxed_text(self):
        '''Tests that multiple different matches (that are not within others) are matched and processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True, False], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_recursive_boxed_text(self):
        '''Tests that multiple different matches (that are contained as content of eachother) are matched and processed correctly.
        '''
        test_string = self.read_test_file(self.processor_name, 'recursive_boxed_text.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'recursive_boxed_text_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_indented_value_no(self):
        '''Tests that indented class not added if indent value is "no".
        '''
        test_string = self.read_test_file(self.processor_name, 'indented_value_no.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'indented_value_no_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_indented_required(self):
        '''Tests to ensure that boxed text tag is rendered correctly when indented argument is required.
        '''
        custom_argument_rules = {
            "boxed-text": {
                "indented": True
            }
        }

        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'indented_required.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [GenericContainerBlockProcessor(self.processor_name, self.ext, Mock()).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'indented_required_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_type_required(self):
        '''Tests to ensure that boxed text tag is rendered correctly when type argument is required.
        '''
        custom_argument_rules = {
            "boxed-text": {
                "type": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'type_required.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [GenericContainerBlockProcessor(self.processor_name, self.ext, Mock()).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'type_required_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_indented_and_type_required(self):
        '''Tests to ensure that boxed text tag is rendered correctly when both indented and type arguments are required.
        '''
        custom_argument_rules = {
            "boxed-text": {
                "indented": True,
                "type": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'indented_and_type_required.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [GenericContainerBlockProcessor(self.processor_name, self.ext, Mock()).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension_custom_rules])
        expected_string = self.read_test_file(self.processor_name, 'indented_and_type_required_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_indented_required_not_provided(self):
        '''Tests to ensure that error is raised when indented argument is required and not given.
        '''
        custom_argument_rules = {
            "boxed-text": {
                "indented": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'indented_required_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [GenericContainerBlockProcessor(self.processor_name, self.ext, Mock()).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    def test_custom_arguments_indented_and_type_required_type_not_provided(self):
        '''Tests to ensure that error is raised when indented and type arguments are required and type is not given.
        '''
        custom_argument_rules = {
            "boxed-text": {
                "indented": True,
                "type": True
            }
        }
        verto_extension_custom_rules = VertoExtension(
            processors=[self.processor_name],
            custom_argument_rules=custom_argument_rules
        )

        test_string = self.read_test_file(self.processor_name, 'indented_and_type_required_type_not_provided.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [GenericContainerBlockProcessor(self.processor_name, self.ext, Mock()).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto_extension_custom_rules]), test_string)

    # ~
    # Doc Tests
    # ~

    def test_doc_example_basic(self):
        '''Tests that the most generic case of a single match is found with generic content contained within.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''Tests and shows example of overriding the html of the processor.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [self.block_processor.test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
