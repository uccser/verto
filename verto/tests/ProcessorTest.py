import unittest
import pkg_resources
import json
import markdown
from verto.VertoExtension import VertoExtension
from markdown.extensions import Extension
from jinja2 import Environment, PackageLoader, select_autoescape
from verto.tests.BaseTest import BaseTest

class ProcessorTest(BaseTest):
    '''A base test class for individual test classes.
    '''

    def __init__(self, *args, **kwargs):
        '''Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display
        on test failures.
        '''
        BaseTest.__init__(self, *args, **kwargs)

    def loadJinjaTemplate(self, template):
        '''Loads a jinja template from the given processor name.
        Args:
            template: the processor name to load the template.
        Returns:
            A jinja template.
        '''
        env = Environment(
                loader=PackageLoader('verto', 'html-templates'),
                autoescape=select_autoescape(['html'])
                )
        jinja_template = env.get_template(template + '.html')
        return jinja_template

    def loadProcessorInfo(self):
        '''Loads the processor info similar to the verto extension.
        '''
        pattern_data = pkg_resources.resource_string('verto', 'processor-info.json').decode('utf-8')
        return json.loads(pattern_data)

    def to_blocks(self, string):
        '''See ParseChunk of markdown.blockparser.BlockParser
        for how text in chunked.
        Args:
            string: The string to break into blocks.
        Returns:
            A list of strings as markdown blocks.
        '''
        return string.split('\n\n')

    def setUp(self):
        '''Runs before each testcase, creates a verto extensions
        and a markdown instance for running tests.
        '''
        self.verto_extension = VertoExtension([self.processor_name], {})
        self.md = markdown.Markdown(extensions=[self.verto_extension])

    def tearDown(self):
        '''Runs after each testcase.
        '''
        self.md = None
