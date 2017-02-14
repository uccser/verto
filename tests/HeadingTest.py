import unittest
import markdown

from kordac.KordacExtension import KordacExtension
from kordac.processors.NumberedHashHeaderProcessor import NumberedHashHeaderProcessor
from kordac.tests.BaseTestCase import BaseTestCase

class HeadingTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'heading'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)
        self.ext.jinja_templates = {self.tag_name: BaseTestCase.loadJinjaTemplate(self, self.tag_name)}
