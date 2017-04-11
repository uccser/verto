from verto.errors.Error import Error


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
