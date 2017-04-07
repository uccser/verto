from verto.tests.BaseTest import BaseTest

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
        pass

    def test_example_simple_void_tag(self):
        '''Checks that a simple (unclosed) void tag is created without
        error.
        '''
        pass

    def test_example_simple_closed_void_tag(self):
        '''Checks that a simple void tag with closing '\' is created
        without error.
        '''
        pass

    def test_example_comment(self):
        '''Checks that comments are added unchanged.
        '''
        pass

    def test_example_ie_comment(self):
        '''Checks that ie comments are added unchanged.
        '''
        pass

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
