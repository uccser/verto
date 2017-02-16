import unittest, os, subprocess
from kordac import Kordac

class SmokeDocsTest(unittest.TestCase):
    """Tests opening of files and that kordac generates some output."""

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None
        self.build_path = "docs/build"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skipIf(
        not os.path.isdir("docs") and os.name not in ['nt', 'posix'],
        "Docs are not present")
    def test_compile_docs(self):
        system = os.name
        # TODO: Cleanup old build
        command = None
        if system == 'nt':
            command = 'make.bat'
        elif system == 'posix':
            command = 'make'

        if command is None:
            self.fail("Unknown operating system, but test still run. This should never happen.")

        p = subprocess.Popen([command, 'clean'], cwd='docs', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=None)
        p.wait(timeout=10) # Will throw exception if times out
        self.assertEqual(p.returncode, 0) # Success returncode

        p = subprocess.Popen([command, 'html'], cwd='docs', stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=None)
        p.wait(timeout=10) # Will throw exception if times out
        self.assertEqual(p.returncode, 0) # Success returncode

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
