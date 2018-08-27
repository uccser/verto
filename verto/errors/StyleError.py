from verto.errors.Error import Error

MESSAGE_TEMPLATE = '''{}
The error occured in the following line(s):
{}
'''


class StyleError(Error):
    '''Exception raised when a Style rule is broken.

    Attributes:
        line_nums: the line numbers the rule as broken on
        lines: lines where the style rule was broken
        message: explanation of why error was thrown
    '''

    def __init__(self, line_nums, lines, message):
        super().__init__(message)
        self.line_nums = line_nums
        self.lines = lines
        self.message = message

    def __str__(self):
        '''Overried default error string.

        Returns:
            Error message for incorrect style, including offending lines.

        '''
        error_lines = ''
        for index, line in enumerate(self.lines):
            error_lines += '{}: {}\n'.format(self.line_nums[index], line)
        return MESSAGE_TEMPLATE.format(self.message, error_lines)
