import markdown
from verto.tests.BaseTest import BaseTest
from verto.VertoExtension import VertoExtension

class MarkdownOverrideTest(BaseTest):
    '''Tests that the overrides for built-in markdown packages
    continue to work as normal markdown.
    '''

    def __init__(self, *args, **kwargs):
        '''Setup asset file directory.
        '''
        super().__init__(*args, **kwargs)
        self.test_type = "markdown-override"

    def read_test_file(self, filename):
        '''Returns a string for a given file.

        Args:
            filename: The filename of the file found in the asset
              directory.
        Returns:
            A string of the given file.
        '''
        return super().read_test_file(self.test_type, filename, True)

    def setUp(self):
        '''Runs before each testcase, creates a verto extensions
        and a markdown instance for running tests.
        '''
        self.verto_extension = VertoExtension([], {})

    def test_unordered_list_asterisk_tight(self):
        '''Check that tight unordered list with asterisks produces expected output.
        '''
        test_string = self.read_test_file('unordered_list_asterisk_tight.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('unordered_list_asterisk_tight_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_unordered_list_asterisk_loose(self):
        '''Check that loose unordered list with asterisks produces expected output.
        '''
        test_string = self.read_test_file('unordered_list_asterisk_loose.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('unordered_list_asterisk_loose_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_unordered_list_tight_nested(self):
        '''Check that tight unordered list with asterisks produces expected output.
        '''
        test_string = self.read_test_file('unordered_list_tight_nested.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('unordered_list_tight_nested_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_unordered_list_loose_nested(self):
        '''Check that loose unordered list with asterisks produces expected output.
        '''
        test_string = self.read_test_file('unordered_list_loose_nested.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('unordered_list_loose_nested_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_unordered_list_mixed_nested(self):
        '''Check that loose unordered list with asterisks produces expected output.
        '''
        test_string = self.read_test_file('unordered_list_mixed_nested.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('unordered_list_mixed_nested_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_ordered_list_tight(self):
        '''Check that tight ordered list with numbers produces expected output.
        '''
        test_string = self.read_test_file('ordered_list_tight.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('ordered_list_tight_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_ordered_list_loose(self):
        '''Check that loose ordered list with numbers produces expected output.
        '''
        test_string = self.read_test_file('ordered_list_loose.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('ordered_list_loose_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_ordered_list_multiple_paragraphs(self):
        '''Check that an ordered list with multiple paragraphs produces expected output.
        '''
        test_string = self.read_test_file('ordered_list_multiple_paragraphs.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('ordered_list_multiple_paragraphs_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_ordered_list_tight_nested(self):
        '''Check that nested tight ordered list with numbers produces expected output.
        '''
        test_string = self.read_test_file('ordered_list_tight_nested.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('ordered_list_tight_nested_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_sane_list(self):
        '''Check that nested tight ordered list with numbers produces expected output.
        '''
        test_string = self.read_test_file('sane_list.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('sane_list_expected.html')
        self.assertEqual(expected_string, converted_test_string)

    def test_sane_list_python_markdown(self):
        '''Check that nested tight ordered list with numbers produces expected output.
        '''
        test_string = self.read_test_file('sane_list_python_markdown.md')
        converted_test_string = markdown.markdown(test_string, extensions=[self.verto_extension])
        expected_string = self.read_test_file('sane_list_python_markdown_expected.html')
        self.assertEqual(expected_string, converted_test_string)
