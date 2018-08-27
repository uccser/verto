import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.ConditionalProcessor import ConditionalProcessor
from verto.errors.TagNotMatchedError import TagNotMatchedError
from verto.tests.ProcessorTest import ProcessorTest


class ConditionalTest(ProcessorTest):
    '''Conditionals expect complex output and need to match
    many possible conditions.

    Note:
        - No tests for custom argument rules because it doesn't
          make sense to require one or more of these arguments
          to be given.
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

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_basic_else_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_elif_no_else(self):
        '''Complex example showing multiple elif statements with
        no else statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_elif_no_else.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'example_elif_no_else_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_elif_no_else_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_example_single_elif(self):
        '''Example showing a single elif statement with no
        else statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_single_elif.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_single_elif_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiple_else_error(self):
        '''Ensures that the TagNotMatchedError is thrown when
        multiple else statements are given.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_else_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_else_then_elif_error(self):
        '''Ensures that the TagNotMatchedError is thrown when
        elifs are given after the else statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'else_then_elif_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_end_statement_error(self):
        '''Ensures that the TagNotMatchedError is thrown
        when the end statement is not matched.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_end_statement_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    def test_missing_if_statement_error(self):
        '''Ensures that the TagNotMatchedError is thrown
        when an else/elif is given before an if statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'missing_if_statement_error.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        self.assertRaises(TagNotMatchedError, lambda x: markdown.markdown(x, extensions=[self.verto_extension]), test_string)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''Basic example showing only a single if statement
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_doc_example_complex(self):
        '''Complex example using multiple elifs and an else
        statement.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_complex_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, False, True, False, True, False, True, False, True], [ConditionalProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
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
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
