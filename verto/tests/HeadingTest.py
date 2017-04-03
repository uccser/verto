import unittest
import markdown
from unittest.mock import Mock

from verto.VertoExtension import VertoExtension
from verto.processors.HeadingBlockProcessor import HeadingBlockProcessor
from verto.tests.ProcessorTest import ProcessorTest
from verto.utils.HeadingNode import HeadingNode

class HeadingTest(ProcessorTest):
    '''The heading processor is a unique processor that replaces the
    functionality of the default markdown (#) heading. We allow for
    an html override and the final result also outputs a tree
    representing the layout of the headings. A consideration when
    creating tests is that slugs of headings are unique.
    '''

    def __init__(self, *args, **kwargs):
        '''Setup for asset loading and match checking.
        '''
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'heading'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_example_blank(self):
        '''Checks to see that if no headings exist the output result
        is empty.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_blank.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([False], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_blank_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = self.verto_extension.get_heading_tree()
        self.assertIsNone(tree)

    def test_single_heading(self):
        '''Checks the simplist case of a single heading.
        '''
        test_string = self.read_test_file(self.processor_name, 'example_single_heading.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'example_single_heading_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = self.verto_extension.get_heading_tree()
        expected_tree = (
            HeadingNode(title='Heading One',
                        title_slug='heading-one',
                        level=1,
                        children=()
            ),
        )
        self.assertTupleEqual(tree, expected_tree)

    def test_multiple_roots_zero_level(self):
        '''Test complex usage of heading where root level nodes
        may be of varying levels until an H1 is used.
        '''
        test_string = self.read_test_file(self.processor_name, 'multiple_roots_zero_level.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True, True, True, True, True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'multiple_roots_zero_level_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = verto_extension.get_heading_tree()
        expected_tree = (HeadingNode(title='This is an H4',
                                    title_slug='this-is-an-h4',
                                    level=4,
                                    children=()
                        ),
                        HeadingNode(title='This is an H2',
                                    title_slug='this-is-an-h2',
                                    level=2,
                                    children=(
                                        HeadingNode(
                                            title='This is an H3',
                                            title_slug='this-is-an-h3',
                                            level=3,
                                            children=()
                                        ),
                                    )
                        ),
                        HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H3',
                                            title_slug='this-is-an-h3-2',
                                            level=3,
                                            children=()
                                        ),
                                        HeadingNode(title='This is an H2',
                                                    title_slug='this-is-an-h2-2',
                                                    level=2,
                                                    children=(
                                                        HeadingNode(title='This is an H4',
                                                                    title_slug='this-is-an-h4-2',
                                                                    level=4,
                                                                    children=()
                                                        ),
                                                    )
                                        ),
                                    )
                        ),
                    )
        self.assertTupleEqual(tree, expected_tree)

    #~
    # Doc Tests
    #~

    def test_doc_example_basic(self):
        '''An example of simplistic useage.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_basic_usage_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = self.verto_extension.get_heading_tree()
        expected_tree = (HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H2',
                                            title_slug='this-is-an-h2',
                                            level=2,
                                            children=(
                                                HeadingNode(
                                                    title='This is an H6',
                                                    title_slug='this-is-an-h6',
                                                    level=6,
                                                    children=()
                                                ),
                                            )
                                        ),
                                    )
                        ),
                    )
        self.assertTupleEqual(tree, expected_tree)


    def test_doc_example_override_html(self):
        '''An example of complex useage, involving multiple H1s
        and shows html overriding.
        '''
        test_string = self.read_test_file(self.processor_name, 'doc_example_override_html.md')
        blocks = self.to_blocks(test_string)

        self.assertListEqual([True, True, True, True, True, True, True], [HeadingBlockProcessor(self.ext, self.md.parser).test(blocks, block) for block in blocks], msg='"{}"'.format(test_string))

        html_template = self.read_test_file(self.processor_name, 'doc_example_override_html_template.html', strip=True)
        verto_extension = VertoExtension([self.processor_name], html_templates={self.processor_name: html_template})

        converted_test_string = markdown.markdown(test_string, extensions=[verto_extension])
        expected_string = self.read_test_file(self.processor_name, 'doc_example_override_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

        tree = verto_extension.get_heading_tree()
        expected_tree = (HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H2',
                                            title_slug='this-is-an-h2',
                                            level=2,
                                            children=(
                                                HeadingNode(
                                                    title='This is an H4',
                                                    title_slug='this-is-an-h4',
                                                    level=4,
                                                    children=()
                                                ),
                                            )
                                        ),
                                    )
                        ),
                        HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1-2',
                                    level=1,
                                    children=(
                                        HeadingNode(
                                            title='This is an H3',
                                            title_slug='this-is-an-h3',
                                            level=3,
                                            children=(
                                                HeadingNode(
                                                    title='This is an H6',
                                                    title_slug='this-is-an-h6',
                                                    level=6,
                                                    children=()
                                                ),
                                            )
                                        ),
                                    )
                        ),
                        HeadingNode(title='This is an H1',
                                    title_slug='this-is-an-h1-3',
                                    level=1,
                                    children=()
                        ),
                    )

        self.assertTupleEqual(tree, expected_tree)
