import unittest
import markdown

from kordac.KordacExtension import KordacExtension
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from tests.BaseTestCase import BaseTestCase

class InteractiveTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'interactive'
        self.ext = Mock()
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)
        self.ext.jinja_templates = {self.tag_name: BaseTestCase.loadJinjaTemplate(self, self.tag_name)}
