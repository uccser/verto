import unittest
from kordac import Kordac

class ConfigurationTest(unittest.TestCase):
    """Test configuration methods of Kordac"""

    def __init__(self, *args, **kwargs):
        """Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        """
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.test_file_path = 'kordac/tests/assets/configuration}/{}'
        self.maxDiff = None

    def test_default_processors_on_creation(self):
        kordac = Kordac()
        default_processors = kordac.processor_defaults()
        self.assertEqual(kordac.kordac_extension.processors, default_processors)

    def test_custom_processors_on_creation(self):
        processors = {'comment', 'image'}
        kordac = Kordac(processors=processors)
        self.assertEqual(kordac.kordac_extension.processors, processors)

    def test_custom_processors_after_creation(self):
        kordac = Kordac()
        processors = kordac.processor_defaults()
        processors.add('example_processor')
        kordac.update_processors(processors)
        self.assertEqual(kordac.kordac_extension.processors, processors)

    def test_unique_custom_processors(self):
        processors = ['comment', 'comment', 'comment']
        kordac = Kordac(processors=processors)
        self.assertEqual(kordac.kordac_extension.processors, set(processors))
        processors = list(kordac.processor_defaults())
        processors.append('example_processor')
        processors.append('example_processor')
        processors.append('example_processor')
        kordac.update_processors(processors)
        self.assertTrue(kordac.kordac_extension.processors, processors)

    def test_custom_templates_on_creation(self):
        custom_templates = {
            'image': '<img />',
            'boxed-text': '<div class="box"></div>'
        }
        kordac = Kordac(html_templates=custom_templates)
        for processor_name, template in custom_templates.items():
            stored_template = kordac.kordac_extension.jinja_templates[processor_name]
            self.assertEqual(template, stored_template)
