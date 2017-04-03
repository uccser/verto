import unittest

class BaseTest(unittest.TestCase):
    '''A base test class for individual test classes.'''

    def __init__(self, *args, **kwargs):
        '''Creates BaseTest Case class.

        Create class inheiriting from TestCase, while also storing
        the path to test files and the maxiumum difference to display on
        test failures.
        '''
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.test_file_path = 'verto/tests/assets/{test_type}/{filename}'
        self.maxDiff = None

    def read_test_file(self, test_type, filename, strip=False):
        '''Returns a string for a given file.

        This function reads a file from a given filename in UTF-8 encoding.
        '''
        file_path = self.test_file_path.format(test_type=test_type, filename=filename)
        file_object = open(file_path, encoding='utf-8')
        text =  file_object.read()
        if strip:
            text = text.rstrip('\r\n')
        return text
