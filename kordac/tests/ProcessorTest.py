import unittest
import json
import markdown
from kordac.KordacExtension import KordacExtension
from markdown.extensions import Extension
from jinja2 import Environment, PackageLoader, select_autoescape
from kordac.tests.BaseTest import BaseTest

class ProcessorTest(BaseTest):
    """A base test class for individual test classes"""

    def __init__(self, *args, **kwargs):
        """Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        """
        BaseTest.__init__(self, *args, **kwargs)

    def loadJinjaTemplate(self, template):
        env = Environment(
                loader=PackageLoader('kordac', 'html-templates'),
                autoescape=select_autoescape(['html'])
                )
        jinja_template = env.get_template(template + '.html')
        return jinja_template

    def loadProcessorInfo(self):
        pattern_data = open('kordac/processor-info.json').read()
        return json.loads(pattern_data)

    def to_blocks(self, string):
        ''' Returns a list of strings as markdown blocks.

        See ParseChunk of markdown.blockparser.BlockParser for how text in chunked.
        '''
        return string.split('\n\n')

    def setUp(self):
        self.kordac_extension = KordacExtension([self.processor_name], {})
        self.md = markdown.Markdown(extensions=[self.kordac_extension])

    def tearDown(self):
        self.md = None
