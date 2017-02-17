import unittest
import markdown

from kordac.KordacExtension import KordacExtension
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from kordac.tests.BaseTestCase import BaseTestCase

class InteractiveTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.processor_name = 'interactive'
        self.ext = Mock()
        self.ext.processor_info = BaseTestCase.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: BaseTestCase.loadJinjaTemplate(self, self.processor_name)}
