import unittest
import markdown

from kordac.KordacExtension import KordacExtension
from kordac.processors.NumberedHashHeaderProcessor import NumberedHashHeaderProcessor
from kordac.tests.BaseTestCase import BaseTestCase

class HeadingTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'heading'
        self.ext = Mock()
        self.ext.processor_patterns = BaseTestCase.loadProcessorPatterns(self)
        self.ext.jinja_templates = {self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name)}
