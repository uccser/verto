import unittest
from kordac import Kordac
import jinja2

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
        # This test doesn't do a perfect check that both templates are the same
        # as we cannot access the raw string stored within the loaded template
        # Instead we check if the rendered version of both is the same, however
        # this doesn't check context variables are the same.
        custom_templates = {
            'image': '<img />',
            'boxed-text': '<div class="box"></div>'
        }
        kordac = Kordac(html_templates=custom_templates)
        for processor_name, template in custom_templates.items():
            expected_template = jinja2.Template(template)
            rendered_expected_template = expected_template.render()
            stored_template = kordac.kordac_extension.jinja_templates[processor_name]
            rendered_stored_template = stored_template.render()
            self.assertEqual(rendered_expected_template, rendered_stored_template)

    def test_custom_templates_after_creation(self):
        # This test doesn't do a perfect check that both templates are the same
        # as we cannot access the raw string stored within the loaded template
        # Instead we check if the rendered version of both is the same, however
        # this doesn't check context variables are the same.
        kordac = Kordac()
        custom_templates = {
            'image': '<img />',
            'boxed-text': '<div class="box"></div>'
        }
        for processor_name, template in custom_templates.items():
            expected_template = jinja2.Template(template)
            rendered_expected_template = expected_template.render()
            stored_template = kordac.kordac_extension.jinja_templates[processor_name]
            rendered_stored_template = stored_template.render()
            self.assertNotEqual(rendered_expected_template, rendered_stored_template)
        kordac.update_templates(custom_templates)
        for processor_name, template in custom_templates.items():
            expected_template = jinja2.Template(template)
            rendered_expected_template = expected_template.render()
            stored_template = kordac.kordac_extension.jinja_templates[processor_name]
            rendered_stored_template = stored_template.render()
            self.assertEqual(rendered_expected_template, rendered_stored_template)

    def test_reset_templates_after_custom(self):
        # This test doesn't do a perfect check that both templates are the same
        # as we cannot access the raw string stored within the loaded template
        # Instead we check if the rendered version of both is the same, however
        # this doesn't check context variables are the same.
        default_template_path = 'kordac/html-templates/{}.html'
        custom_templates = {
            'image': '<img />',
            'boxed-text': '<div class="box"></div>'
        }
        kordac = Kordac(html_templates=custom_templates)
        for processor_name, template in custom_templates.items():
            expected_template = jinja2.Template(template)
            rendered_expected_template = expected_template.render()
            stored_template = kordac.kordac_extension.jinja_templates[processor_name]
            rendered_stored_template = stored_template.render()
            self.assertEqual(rendered_expected_template, rendered_stored_template)
        kordac.default_templates()
        for processor_name in custom_templates.keys():
            default_template = open(default_template_path.format(processor_name), 'r').read()
            expected_template = jinja2.Template(default_template)
            rendered_expected_template = expected_template.render()
            stored_template = kordac.kordac_extension.jinja_templates[processor_name]
            rendered_stored_template = stored_template.render()
            self.assertEqual(rendered_expected_template, rendered_stored_template)
