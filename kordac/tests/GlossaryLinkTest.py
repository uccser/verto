import markdown
import re
from unittest.mock import Mock
from kordac.KordacExtension import KordacExtension
from kordac.processors.GlossaryLinkPattern import GlossaryLinkPattern
from kordac.tests.ProcessorTest import ProcessorTest


class GlossaryLinkTest(ProcessorTest):

    def __init__(self, *args, **kwargs):
        """Set processor name in class for file names"""
        ProcessorTest.__init__(self, *args, **kwargs)
        self.processor_name = 'glossary-link'
        self.ext = Mock()
        self.ext.processor_info = ProcessorTest.loadProcessorInfo(self)
        self.ext.jinja_templates = {self.processor_name: ProcessorTest.loadJinjaTemplate(self, self.processor_name)}

    def test_single_word_term(self):
        test_string = self.read_test_file(self.processor_name, 'single_word_term.md')

        processor = GlossaryLinkPattern(self.ext, self.md.parser)
        print(re.search(processor.compiled_re, test_string))
        self.assertIsNotNone(re.search(processor.compiled_re, test_string))

        converted_test_string = markdown.markdown(test_string, extensions=[self.kordac_extension])
        expected_string = self.read_test_file(self.processor_name, 'single_word_term_expected.html', strip=True).strip()
        self.assertEqual(expected_string, converted_test_string)


