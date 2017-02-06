import unittest
import markdown

from KordacExtension import KordacExtension
from kordac.processors.InteractiveBlockProcessor import InteractiveBlockProcessor
from tests.BaseTestCase import BaseTestCase

class InteractiveTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'interactive'
        self.ext.tag_patterns = BaseTestCase.loadTagPatterns(self)