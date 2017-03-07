import unittest
from kordac import Kordac
import jinja2
from kordac.tests.BaseTest import BaseTest

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
