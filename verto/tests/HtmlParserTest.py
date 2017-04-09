from verto.tests.BaseTest import BaseTest
from verto.utils.HtmlParser import HtmlParser
from markdown.util import etree
class HtmlParserTest(BaseTest):

    def __init__(self, *args, **kwargs):
        '''Setup asset file directory.
        '''
        super().__init__(*args, **kwargs)
        self.test_type = "html-parser"

    def read_test_file(self, filename):
        '''Returns a string for a given file.

        Args:
            filename: The filename of the file found in the asset
              directory.
        Returns:
            A string of the given file.
        '''
        return super().read_test_file(self.test_type, filename, True)

    # ~
    # Valid Examples
    # ~

    def test_example_basic_usage(self):
        '''Checks that the expected usecase works.
        '''
        input_text = self.read_test_file('example_basic_usage.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        root_string = etree.tostring(root, encoding='unicode', method='html')
        self.assertEquals(input_text, root_string)

    def test_example_simple_void_tag(self):
        '''Checks that a simple (unclosed) void tag is created without
        error.
        '''
        input_text = self.read_test_file('example_simple_void_tag.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        root_string = etree.tostring(root, encoding='unicode', method='html')
        self.assertEquals(input_text, root_string)

    def test_example_simple_closed_void_tag(self):
        '''Checks that a simple void tag with closing '\' is created
        without error.
        '''
        input_text = self.read_test_file('example_simple_closed_void_tag.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        root_string = etree.tostring(root, encoding='unicode', method='html')
        expected_text = self.read_test_file('example_simple_void_tag.html')
        self.assertEquals(expected_text, root_string)

    def test_example_comment(self):
        '''Checks that comments are added unchanged.
        '''
        input_text = self.read_test_file('example_comment.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        root_string = etree.tostring(root, encoding='unicode', method='html')
        self.assertEquals(input_text, root_string)

    def test_example_comment_ie(self):
        '''Checks that ie comments are added unchanged.
        '''
        input_text = self.read_test_file('example_comment_ie.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        root_string = etree.tostring(root, encoding='unicode', method='html')
        self.assertEquals(input_text, root_string)

    def test_example_data_and_subelements(self):
        '''Checks that data and subelements work together.
        '''
        input_text = self.read_test_file('example_data_and_subelements.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        root_string = etree.tostring(root, encoding='unicode', method='html')
        self.assertEquals(input_text, root_string)

    # ~
    # Invalid Examples
    # ~

    def test_example_multiple_roots_error(self):
        '''Checks that when multiple roots are detected that an exception
        is raised.
        '''
        pass

    def test_example_lone_end_tag_error(self):
        '''Checks that lone end tags cause an exception to be raised.
        '''
        pass

    def test_example_missing_end_tag_error(self):
        '''Checks that elements (that need to be closed) cause an
        exception to be raised.
        '''
        pass

    def test_example_missing_end_tag_implicit_error(self):
        '''Checks that elements (that need to be closed) cause an
        exception to be raised, when they are implicitly closed
        by an outer closing tag.
        '''
        pass

    def test_example_data_without_tags_error(self):
        '''Checks that data without a root tag causes an exception to
        be raised.
        '''
        pass
