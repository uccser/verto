from verto.processors.errors.Error import Error


class StyleError(Error):
    '''Exception raised when a Style rule is broken.

    Attributes:
        rule -- rule which was broken
        lines -- lines where the style rule was broken
        message -- explanation of why error was thrown
    '''

    def __init__(self, line_nums, lines, message):
        super().__init__(message)
        self.line_nums = line_nums
        self.lines = lines
        self.message = message
