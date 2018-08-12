import markdown

from verto.Verto import Verto, VertoResult
from verto.VertoExtension import VertoExtension
from verto.processors.ScratchTreeprocessor import ScratchImageMetaData
from verto.utils.HeadingNode import HeadingNode
from verto.tests.BaseTest import BaseTest
from verto.errors.ArgumentMissingError import ArgumentMissingError
from verto.errors.CustomArgumentRulesError import CustomArgumentRulesError


class ConfigurationTest(BaseTest):
    '''Test configuration methods of Verto

    These are not true unit tests, as they create the complete Verto
    system, however we are using the unittest framework for ease of
    use and simplicity of our testing suite.
    '''

    def __init__(self, *args, **kwargs):
        '''Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display
        on test failures.
        '''
        BaseTest.__init__(self, *args, **kwargs)
        self.test_name = 'configuration'
        self.maxDiff = None
        self.custom_templates = {
            'image': '<img alt=\'test\' class=\'test\'/>',
            'boxed-text': '<div class=\'box\'>{% autoescape false %}{{ text }}{% endautoescape %}</div>',
            'video-youtube': 'https://www.youtube.com/embed/{{ identifier  }}?rel=0'
        }

    def test_multiple_calls(self):
        '''Checks all fields of VertoResult are correct for multiple Verto calls.
        '''
        test_cases = [(
            'all_processors.md',
            VertoResult(
                html_string=self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True),
                title='Example Title',
                required_files={
                    'interactives': {
                        'binary-cards'
                    },
                    'images': set(),
                    'page_scripts': set(),
                    'scratch_images': {
                        ScratchImageMetaData(
                            hash='a0f8fcad796864abfacac8bda6e0719813833fd1fca348700abbd040557c1576',
                            text='when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees'
                        ),
                    }
                },
                heading_tree=(
                    HeadingNode(
                        title='Example Title',
                        title_slug='example-title',
                        level=1,
                        children=(),
                    ),
                    HeadingNode(
                        title='Example Title 2',
                        title_slug='example-title-2',
                        level=1,
                        children=()
                    ),
                ),
                required_glossary_terms={
                    'algorithm': []
                }
            )
        ), (
            'some_processors.md',
            VertoResult(
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
        ), (
            'some_processors_2.md',
            VertoResult(
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
                    'hello': [],
                    'algorithm':
                        [('computer program', 'glossary-algorithm'),
                         ('algorithm cost', 'glossary-algorithm-2'),
                         ('searching algorithms', 'glossary-algorithm-3'),
                         ('sorting algorithms', 'glossary-algorithm-4')]
                }
            )
        )]

        verto = Verto()
        for filename, expected_result in test_cases:
            test_string = self.read_test_file(self.test_name, filename)
            verto_result = verto.convert(test_string)

            self.assertEqual(verto_result.title, expected_result.title)
            self.assertEqual(verto_result.required_files, expected_result.required_files)
            self.assertTupleEqual(verto_result.heading_tree, expected_result.heading_tree)
            self.assertDictEqual(verto_result.required_glossary_terms, expected_result.required_glossary_terms)
            verto.clear_saved_data()

    def test_multiple_calls_without_clearing(self):
        '''Tests that if the verto extension is not cleared that information such as required_files and slugs are persistent.
        '''
        filename = 'all_processors.md'
        other_filename = 'otherfile.md'
        expected_result = VertoResult(
            html_string=self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True),
            title='Example Title',
            required_files={
                'interactives': {
                    'binary-cards'
                },
                'images': set(),
                'page_scripts': set(),
                'scratch_images': {
                    ScratchImageMetaData(
                        hash='a0f8fcad796864abfacac8bda6e0719813833fd1fca348700abbd040557c1576',
                        text='when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees'
                    ),
                }
            },
            heading_tree=(
                HeadingNode(
                    title='Example Title',
                    title_slug='example-title',
                    level=1,
                    children=(),
                ),
                HeadingNode(
                    title='Example Title 2',
                    title_slug='example-title-2',
                    level=1,
                    children=()
                ),
            ),
            required_glossary_terms={
                'algorithm': []
            }
        )
        expected_otherfile_result = VertoResult(
            html_string=self.read_test_file(self.test_name, 'otherfile_expected.html', strip=True),
            title='Example Title',
            required_files={
                'interactives': {
                    'binary-cards'
                },
                'images': {
                    'pixel-diamond.png'
                },
                'page_scripts': set(),
                'scratch_images': {
                    ScratchImageMetaData(
                        hash='a0f8fcad796864abfacac8bda6e0719813833fd1fca348700abbd040557c1576',
                        text='when flag clicked\nclear\nforever\npen down\nif <<mouse down?> and <touching [mouse-pointer v]?>> then\nswitch costume to [button v]\nelse\nadd (x position) to [list v]\nend\nmove (foo) steps\nturn ccw (9) degrees'
                    ),
                    ScratchImageMetaData(
                        hash='b78bff524e54a18116e1e898a93e360827f874a8b0b508e1edc47d21516495ad',
                        text='never\ngoing\nto\ngive\nyou\nup'
                    ),
                }
            },
            heading_tree=(HeadingNode(
                title='Example Title',
                title_slug='example-title-3',
                level=1,
                children=(),
            ),
            ),
            required_glossary_terms={
                'algorithm': []
            }
        )

        verto = Verto()
        # First file
        test_string = self.read_test_file(self.test_name, filename)
        verto_result = verto.convert(test_string)

        self.assertEqual(verto_result.title, expected_result.title)
        self.assertEqual(verto_result.required_files, expected_result.required_files)
        self.assertTupleEqual(verto_result.heading_tree, expected_result.heading_tree)
        self.assertDictEqual(verto_result.required_glossary_terms, expected_result.required_glossary_terms)

        # Another file
        test_string = self.read_test_file(self.test_name, other_filename)
        verto_result = verto.convert(test_string)

        self.assertEqual(verto_result.title, expected_otherfile_result.title)
        self.assertEqual(verto_result.required_files, expected_otherfile_result.required_files)
        self.assertTupleEqual(verto_result.heading_tree, expected_otherfile_result.heading_tree)
        self.assertDictEqual(verto_result.required_glossary_terms, expected_otherfile_result.required_glossary_terms)

    def test_custom_processors_and_custom_templates_on_creation(self):
        '''Checks if custom processors and custom templates work together on creation of verto.
        '''
        processors = {'image-tag', 'boxed-text'}
        verto = Verto(processors=processors, html_templates=self.custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'custom_processors_custom_templates_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_processors_and_custom_templates_after_creation(self):
        '''Checks if custom processors and custom templates work together after creation of verto.
        '''
        processors = {'image-tag', 'boxed-text'}
        verto = Verto()
        verto.update_processors(processors)
        verto.update_templates(self.custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'custom_processors_custom_templates_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_default_processors_on_creation(self):
        '''Checks if all expected default processors work on default creation.
        '''
        verto = Verto()
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_processors_on_creation(self):
        '''Checks if system only uses specified processors.
        '''
        processors = {'panel', 'image-container'}
        verto = Verto(processors=processors)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'custom_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_processors_after_creation(self):
        '''Checks if extension correct changes processors.
        '''
        verto = Verto()
        processors = Verto.processor_defaults()
        processors.add('example_processor')
        processors.remove('comment')
        verto.update_processors(processors)
        # Check example_processor is now stored in extension processors
        self.assertEqual(verto.verto_extension.processors, processors)
        # Check comments are now skipped
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_except_comment_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_unique_custom_processors(self):
        '''Checks if unique processors are stored when duplicates provided.
        '''
        processors = ['comment', 'comment', 'comment']
        verto = Verto(processors=processors)
        self.assertEqual(verto.verto_extension.processors, set(processors))
        processors = list(Verto.processor_defaults())
        processors.append('example_processor')
        processors.append('example_processor')
        processors.append('example_processor')
        verto.update_processors(processors)
        self.assertTrue(verto.verto_extension.processors, processors)

    def test_custom_templates_on_creation(self):
        '''Checks custom templates are used when given on creation.
        '''
        verto = Verto(html_templates=self.custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_custom_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_templates_after_creation(self):
        '''Checks custom templates are used when given after creation.
        '''
        verto = Verto()
        verto.update_templates(self.custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_custom_html_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_reset_templates_after_custom(self):
        '''Checks custom templates are reset when given at creation.
        '''
        verto = Verto(html_templates=self.custom_templates)
        verto.clear_templates()
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_multiline_custom_templates(self):
        '''Checks that multiple multiline custom templates are loaded and used correctly.
        '''
        custom_templates = {
            'image': \
'''<div class="text-center">
<img src="{{ full_file_path }}" class="rounded img-thumbnail"/>
</div>''',

            'boxed-text': \
'''<div class="card">
<div class="card-block">
{{ text }}
</div>
</div>''',

            'heading': \
'''<{{ heading_type }} id="{{ title_slug }}">
<span class="section_number">
{{ level_1 }}.{{ level_2 }}.{{ level_3 }}.{{ level_4 }}.{{ level_5 }}.{{ level_6 }}.
</span>
{{ title }}
</{{ heading_type }}>'''

        }

        verto = Verto(html_templates=custom_templates)
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'multiline_templates_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_arguments_rules_on_creation(self):
        '''Checks if tag arguments are updated.
        '''
        custom_argument_rules = {
            "image-tag": {
                "alt": False
            }
        }
        verto = Verto(custom_argument_rules=custom_argument_rules)
        self.assertEqual(verto.verto_extension.custom_argument_rules, dict(custom_argument_rules))

    def test_custom_argument_rules_for_multiple_tags(self):
        '''Checks that md file is correctly parsed when multiple tags have custom argument rules.
        '''
        custom_argument_rules = {
            "image-tag": {
                "alt": False
            },
            "panel": {
                "subtitle": True
            }
        }
        verto = Verto(custom_argument_rules=custom_argument_rules)
        self.assertEqual(verto.verto_extension.custom_argument_rules, dict(custom_argument_rules))
        test_string = self.read_test_file(self.test_name, 'all_processors.md')
        converted_test_string = verto.convert(test_string).html_string
        expected_string = self.read_test_file(self.test_name, 'all_processors_expected.html', strip=True)
        self.assertEqual(expected_string, converted_test_string)

    def test_custom_argument_rules_for_multiple_tags_error(self):
        '''Checks that error is raised when a tag's custom argument rules are not followed.
        '''
        custom_argument_rules = {
            "panel": {
                "subtitle": True
            },
            "image-tag": {
                "alt": False
            }
        }
        processors = {'image-tag', 'panel', 'comment'}
        verto = VertoExtension(processors=processors, custom_argument_rules=custom_argument_rules)

        test_string = self.read_test_file(self.test_name, 'custom_argument_rules_multiple_tags_error.md')
        self.assertRaises(ArgumentMissingError, lambda x: markdown.markdown(x, extensions=[verto]), test_string)

    def test_custom_argument_rules_incorrect_processor_error(self):
        '''Checks that error is raised when a processor given in custom argument rules does not exist.
        '''
        custom_argument_rules = {
            "panel": {
                "totallyrealargument": True
            },
            "image-tag": {
                "alt": False
            }
        }
        processors = {'image-tag', 'panel', 'comment'}

        self.assertRaises(CustomArgumentRulesError, lambda: VertoExtension(processors=processors, custom_argument_rules=custom_argument_rules))

    def test_custom_argument_rules_incorrect_processor_argument_error(self):
        '''Checks that error is raised when a processor given in custom argument rules does not exist.
        '''
        custom_argument_rules = {
            "panl": {
                "subtitle": True
            },
            "image-tag": {
                "alt": False
            }
        }
        processors = {'image-tag', 'panel', 'comment'}

        self.assertRaises(CustomArgumentRulesError, lambda: VertoExtension(processors=processors, custom_argument_rules=custom_argument_rules))
