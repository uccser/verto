import unittest
from kordac import Kordac

class ConfigurationTest(unittest.TestCase):
    """Test configuration methods of Kordac"""

    def __init__(self, *args, **kwargs):
        """Creates BaseTest Case class

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        """
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.test_file_path = 'kordac/tests/assets/configuration}/{}'
        self.maxDiff = None

    def test_custom_processors_on_creation(self):
        processors = ['comment', 'image']
        kordac = Kordac(processors=processors)
        self.assertTrue(kordac.kordac_extension.processors, processors)
