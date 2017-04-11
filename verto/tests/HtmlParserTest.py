from verto.tests.BaseTest import BaseTest
from verto.utils.HtmlParser import HtmlParser
from verto.utils.HtmlSerializer import HtmlSerializer
from verto.errors.HtmlParseError import HtmlParseError
from markdown.util import etree


class HtmlParserTest(BaseTest):
    '''Tests that the HtmlParser and HtmlSerializer can be used to
    take in an produce the same HTML string.
    '''

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
        self.assertEquals('html', root.tag)

        elements = list(root)
        self.assertEquals(1, len(elements))
        self.assertEquals('body', elements[0].tag)

        elements = list(elements[0])  # Open Body
        self.assertEquals(3, len(elements))
        self.assertEquals('h1', elements[0].tag)
        self.assertEquals('p', elements[1].tag)
        self.assertEquals('div', elements[2].tag)

        elements = list(elements[2])  # Open Div
        self.assertEquals(2, len(elements))
        self.assertEquals('img', elements[0].tag)
        self.assertEquals('a', elements[1].tag)

        img = elements[0]
        self.assertEquals('Example text.', img.get('alt'))
        self.assertEquals('example.com/example.jpg', img.get('src'))

        a = elements[1]
        self.assertEquals('https://www.example.com', a.get('href'))

        root_string = HtmlSerializer.tostring(root)
        self.assertEquals(input_text, root_string)

    def test_example_simple_void_tag(self):
        '''Checks that a simple (unclosed) void tag is created without
        error.
        '''
        input_text = self.read_test_file('example_simple_void_tag.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        self.assertEquals('img', root.tag)
        self.assertEquals('Example text.', root.get('alt'))
        self.assertEquals('example.com/example.jpg', root.get('src'))

        root_string = HtmlSerializer.tostring(root)
        self.assertEquals(input_text, root_string)

    def test_example_simple_closed_void_tag(self):
        '''Checks that a simple void tag with closing '\' is created
        without error.
        '''
        input_text = self.read_test_file('example_simple_closed_void_tag.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        self.assertEquals('img', root.tag)
        self.assertEquals('Example text.', root.get('alt'))
        self.assertEquals('example.com/example.jpg', root.get('src'))

        root_string = HtmlSerializer.tostring(root)
        expected_text = self.read_test_file('example_simple_void_tag.html')
        self.assertEquals(expected_text, root_string)

    def test_example_comment(self):
        '''Checks that comments are added unchanged.
        '''
        input_text = self.read_test_file('example_comment.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        self.assertEquals(etree.Comment, root.tag)

        root_string = HtmlSerializer.tostring(root)
        self.assertEquals(input_text, root_string)

    def test_example_comment_ie(self):
        '''Checks that ie comments are added unchanged.
        '''
        input_text = self.read_test_file('example_comment_ie.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()

        self.assertEquals(etree.Comment, root.tag)

        root_string = HtmlSerializer.tostring(root)
        self.assertEquals(input_text, root_string)

    def test_example_data_and_subelements(self):
        '''Checks that data and subelements work together.
        '''
        input_text = self.read_test_file('example_data_and_subelements.html')
        parser = HtmlParser()
        parser.feed(input_text).close()
        root = parser.get_root()
        self.assertEquals('html', root.tag)

        elements = list(root)
        self.assertEquals(1, len(elements))
        self.assertEquals('body', elements[0].tag)

        elements = list(elements[0])  # Open Body
        self.assertEquals(2, len(elements))
        self.assertEquals('h1', elements[0].tag)
        self.assertEquals('p', elements[1].tag)

        elements = list(elements[1])  # Open p
        self.assertEquals(3, len(elements))
        self.assertEquals('em', elements[0].tag)
        self.assertEquals('b', elements[1].tag)
        self.assertEquals('a', elements[2].tag)

        root_string = HtmlSerializer.tostring(root)
        self.assertEquals(input_text, root_string)

    # ~
    # Invalid Examples
    # ~

    def test_example_access_root_before_feed_error(self):
        '''Checks that the AttributeError is raised is the root element
        is accessed before it is created.
        '''
        parser = HtmlParser()
        with self.assertRaises(AttributeError):
            parser.get_root()

    def test_example_multiple_roots_error(self):
        '''Checks that when multiple roots are detected that an exception
        is raised.
        '''
        input_text = self.read_test_file('example_multiple_roots_error.html')
        parser = HtmlParser()
        with self.assertRaises(HtmlParseError):
            parser.feed(input_text).close()

    def test_example_lone_end_tag_error(self):
        '''Checks that lone end tags cause an exception to be raised.
        '''
        input_text = self.read_test_file('example_lone_end_tag_error.html')
        parser = HtmlParser()
        with self.assertRaises(HtmlParseError):
            parser.feed(input_text).close()

    def test_example_missing_end_tag_error(self):
        '''Checks that elements (that need to be closed) cause an
        exception to be raised.
        '''
        input_text = self.read_test_file('example_missing_end_tag_error.html')
        parser = HtmlParser()
        with self.assertRaises(HtmlParseError):
            parser.feed(input_text).close()

    def test_example_missing_end_tag_implicit_error(self):
        '''Checks that elements (that need to be closed) cause an
        exception to be raised, when they are implicitly closed
        by an outer closing tag.
        '''
        input_text = self.read_test_file('example_missing_end_tag_implicit_error.html')
        parser = HtmlParser()
        with self.assertRaises(HtmlParseError):
            parser.feed(input_text).close()

    def test_example_data_without_tags_error(self):
        '''Checks that data without a root tag causes an exception to
        be raised.
        '''
        input_text = self.read_test_file('example_data_without_tags_error.html')
        parser = HtmlParser()
        with self.assertRaises(HtmlParseError):
            parser.feed(input_text).close()
