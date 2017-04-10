import unittest, os, subprocess
import pkg_resources
from verto import Verto

class SmokeDocsTest(unittest.TestCase):
    '''Tests that docs build if they are found.'''

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None
        self.build_path = 'docs/build'

    @unittest.skipIf(not pkg_resources.resource_isdir('verto', 'docs') and os.name not in ['nt', 'posix'], 'Docs are not present')
    def test_compile_docs(self):
        '''This test is skipped if the docs directory is not found.
        '''
        cwd = os.path.abspath('docs')
        command = 'make'
        options = 'SPHINXOPTS=\'-W\''

        p = subprocess.Popen([command, 'clean'],
                             cwd=cwd,
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             stderr=None,
                             shell=True)
        p.wait(timeout=10) # Will throw exception if times out
        self.assertEqual(p.returncode, 0) # Success returncode

        p = subprocess.Popen([command, options, 'html'],
                             cwd=cwd,
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL,
                             stderr=None,
                             shell=True)
        p.wait(timeout=10) # Will throw exception if times out
        self.assertEqual(p.returncode, 0) # Success returncode

class SmokeFileTest(unittest.TestCase):
    '''Tests opening of files and that verto generates some output.'''

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.maxDiff = None
        self.verto = None
        self.assets_template = 'tests/assets/smoke/{}'

    def setUp(self):
        '''Run before any testcases.
        '''
        self.verto = Verto()

    def tearDown(self):
        '''Run after any testcases.
        '''
        self.verto = None

    def test_compile_files(self):
        '''Tests that some example files are converted.
        '''
        for chapter in ['algorithms.md', 'introduction.md']:
            text = pkg_resources.resource_string('verto', self.assets_template.format(chapter)).decode('utf-8')
            result = self.verto.convert(text)

            self.assertIsNot(result, None)
            self.assertIsNot(result.title, None)
            self.assertIsNot(result.html_string, None)
            self.assertTrue(len(result.html_string) > 0)

    def test_compile_files_custom(self):
        '''Tests that some example files are converted with custom
        html-templates.
        '''
        custom_templates = {
            'image': '<img />',
            'boxed-text': '<div class="box"></div>'
        }

        verto = Verto(html_templates=custom_templates)
        for chapter in ['algorithms.md', 'introduction.md']:
            text = pkg_resources.resource_string('verto', self.assets_template.format(chapter)).decode('utf-8')
            result = verto.convert(text)

            self.assertIsNot(result, None)
            self.assertIsNot(result.title, None)
            self.assertIsNot(result.html_string, None)
            self.assertTrue(len(result.html_string) > 0)
