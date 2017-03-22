import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.ConditionalProcessor import ConditionalProcessor
from kordac.tests.ProcessorTest import ProcessorTest


class ConditionalTest(ProcessorTest):
    '''Conditionals expect complex output and need to match
    many possible conditions.
    '''

    def __init__(self, *args, **kwargs):
        '''Setup basic information for asset directory.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'conditional'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_example_basic_else(self):
        '''Simple example ensuring else statements works.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_basic_else_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_basic_else_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_elif_noelse(self):
        '''Complex example showing multiple elif statements with
        no else statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_elif_noelse.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'example_elif_noelse_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_elif_noelse_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''Basic example showing only a single if statement
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_complex(self):
        '''Complex example using multiple elifs and an else
        statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_complex_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_complex_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_override_html(self):
        '''Complex example using all features and checking that it
        works with custom templates.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        kordac_extension = KordacExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
