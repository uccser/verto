import unittest
from kordac import Kordac

class SmokeFileTest(unittest.TestCase):
    """Tests opening of files and that kordac generates some output."""

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None
        self.kordac = None
        self.assets_template = 'kordac/tests/assets/smoke/{}'

    def setUp(self):
        self.kordac = Kordac()

    def tearDown(self):
        self.kordac = None

    def test_compile_files(self):
        for chapter in ['algorithms.md', 'introduction.md']:
            with open(self.assets_template.format(chapter), 'r') as f:
                text = f.read()
                result = self.kordac.convert(text)

                self.assertIsNot(result, None)
                self.assertIsNot(result.title, None)
                self.assertIsNot(result.html_string, None)
                self.assertTrue(len(result.html_string) > 0)
