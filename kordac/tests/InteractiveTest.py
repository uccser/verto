import unittest
import markdown

from kordac.KordacExtension import KordacExtension
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest

class InteractiveTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'interactive'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
