import unittest
import markdown

from kordac.KordacExtension import KordacExtension
from kordac.processors.NumberedHashHeaderProcessor import NumberedHashHeaderProcessor
from kordac.tests.ProcessorTest import ProcessorTest

class HeadingTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'heading'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
