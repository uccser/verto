from verto.tests.BaseTest import BaseTest


class MarkdownOverrideTest(BaseTest):
    '''Tests that the HtmlParser and HtmlSerializer can be used to
    take in an produce the same HTML string.
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
