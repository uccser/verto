import unittest
from kordac.Kordac import Kordac, KordacResult
from kordac.utils.HeadingNode import HeadingNode
import jinja2
from kordac.tests.BaseTest import BaseTest
from collections import defaultdict

class ConfigurationTest(BaseTest):
    """Test configuration methods of Kordac

    These are not true unit tests, as they create the complete Kordac system,
    however we are using the unittest framework for ease of use and simplicity
    of our testing suite.
    """

    def __init__(self, *args, **kwargs):
        """Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        """
        BaseTest.__init__(self, *args, **kwargs)
        self.test_name = 'configuration'
        self.maxDiff = None
        self.custom_templates = {
            "image": "<img class='test'/>",
            "boxed-text": "<div class='box'>{% autoescape false %}{{ text }}{% endautoescape %}</div>"
        }

    def test_multiple_calls(self):
        """Checks all fields of KordacResult are correct for multiple Kordac calls"""
        test_cases = [
            ('all_processors.md',
                KordacResult(
                    html_string=self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True),
                    title='Example Title',
                    required_files={
                        'interactives': set(),
                        'images': set(),
                        'page_scripts': set(),
                        'scratch_images': set()
                    },
                    heading_tree=(HeadingNode(
                        title='Example Title',
                        title_slug='example-title',
                        level=1,
                        children=()
                    ),),
                    required_glossary_terms=defaultdict(list)
                )
            ),
            ('some_processors.md',
                KordacResult(
                    html_string=self.read_test_file(self.test_name, 'some_processors_expected.html', strip=True),
                    title='Another Example Title',
                    required_files={
                        'interactives': set(),
                        'images': {'totally-legit-image.png'},
                        'page_scripts': set(),
                        'scratch_images': set()
                    },
                    heading_tree=(HeadingNode(
                        title='Another Example Title',
                        title_slug='another-example-title',
                        level=1,
                        children=(HeadingNode(
                            title='This is an H2',
                            title_slug='this-is-an-h2',
                            level=2,
                            children=()
                        ),),
                    ),),
                    required_glossary_terms={
                        'chomsky-hierarchy':
                            [('Formal languages', 'glossary-chomsky-hierarchy')]
                    }
                )
            ),
            ('some_processors_2.md',
                KordacResult(
                    html_string=self.read_test_file(self.test_name, 'some_processors_2_expected.html', strip=True),
                    title='Another Example Title',
                    required_files={
                        'interactives': set(),
                        'images': {
                            'totally-legit-image.png',
                            'finite-state-automata-no-trap-example.png',
                            'finite-state-automata-trap-added-example.png',
                            'finite-state-automata-trap-added-extreme-example.png',
                            },
                        'page_scripts': set(),
                        'scratch_images': set()
                    },
                    heading_tree=(HeadingNode(
                        title='Another Example Title',
                        title_slug='another-example-title',
                        level=1,
                        children=(),
                    ),),
                    required_glossary_terms={
                        'algorithm':
                            [('computer program', 'glossary-algorithm'),
                             ('algorithm cost', 'glossary-algorithm-2'),
                             ('searching algorithms', 'glossary-algorithm-3'),
                             ('sorting algorithms', 'glossary-algorithm-4')]
                    }
                )
            )
        ]

        for test in test_cases:
            kordac = Kordac()
            test_string = self.read_test_file(self.test_name, test[0])
            kordac_result = kordac.convert(test_string)

            self.assertEqual(kordac_result.title, test[1].title)
            self.assertEqual(kordac_result.required_files, test[1].required_files)
            self.assertTupleEqual(kordac_result.heading_tree, test[1].heading_tree)
            self.assertDictEqual(kordac_result.required_glossary_terms, test[1].required_glossary_terms)


    def test_default_processors_on_creation(self):
        """Checks if all expected default processors work on default creation"""
        kordac = Kordac()
        # kordac.clear_templates()
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_processors_on_creation(self):
        """Checks if system only uses specified processsors"""
        processors = {'panel', 'image'}
        kordac = Kordac(processors=processors)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'custom_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_processors_after_creation(self):
        """Checks if extension correct changes processors"""
        kordac = Kordac()
        processors = Kordac.processor_defaults()
        processors.add('example_processor')
        processors.remove('comment')
        kordac.update_processors(processors)
        # Check example_processor is now stored in extension processors
        self.assertEqual(kordac.kordac_extension.processors, processors)
        # Check comments are now skipped
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_except_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_unique_custom_processors(self):
        """Checks if unique processors are stored when duplicates provided"""
        processors = ['comment', 'comment', 'comment']
        kordac = Kordac(processors=processors)
        self.assertEqual(kordac.kordac_extension.processors, set(processors))
        processors = list(Kordac.processor_defaults())
        processors.append('example_processor')
        processors.append('example_processor')
        processors.append('example_processor')
        kordac.update_processors(processors)
        self.assertTrue(kordac.kordac_extension.processors, processors)

    def test_custom_templates_on_creation(self):
        """Checks custom templates are used when given on creation"""
        kordac = Kordac(html_templates=self.custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_custom_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_templates_after_creation(self):
        """Checks custom templates are used when given after creation"""
        kordac = Kordac()
        kordac.update_templates(self.custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_custom_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_reset_templates_after_custom(self):
        """Checks custom templates are reset when given at creation"""
        kordac = Kordac(html_templates=self.custom_templates)
        kordac.clear_templates()
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiline_custom_templates(self):
        custom_templates = {
            "image": """<div class="text-center">
                          <img src="{{ file_path }}" class="rounded img-thumbnail"/>
                        </div>""",
            "boxed-text": """<div class="card">
                               <div class="card-block">
                                 {{ text }}
                               </div>
                             </div>""",
            "heading": """<{{ heading_type }} id="{{ title_slug }}">
                            <span class="section_number">
                              {{ level_1 }}.{{ level_2 }}.{{ level_3 }}.{{ level_4 }}.{{ level_5 }}.{{ level_6 }}.
                            </span>
                            {{ title }}
                          </{{ heading_type }}>"""
        }

        kordac = Kordac(html_templates=custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = kordac.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'multiline_templates_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)
