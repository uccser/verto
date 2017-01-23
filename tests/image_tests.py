import unittest
import markdown

from csfg_extension import CSFGExtension
from processors.image import *
from tests.BaseTestCase import BaseTestCase

class ImageTest(BaseTestCase):

    def __init__(self, *args, **kwargs):
        """Set tag name in class for file names"""
        BaseTestCase.__init__(self, *args, **kwargs)
        self.tag_name = 'image'
