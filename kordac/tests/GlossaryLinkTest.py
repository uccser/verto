import markdown
from unittest.mock import Mock

from kordac.KordacExtension import KordacExtension
from kordac.processors.GlossaryLinkBlockProcessor import GlossaryLinkBlockProcessor
from kordac.tests.ProcessorTest import ProcessorTest


class GlossaryLinkTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'glossary-link'
        self.ext = Mock()
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)

