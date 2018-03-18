from verto.errors.Error import Error

MESSAGE_TEMPLATE = """{}
Error happened on line {}.
"""


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
        """Overried default error string.

        Returns:
            Error message for incorrect style, including offending lines.

        """
        return MESSAGE_TEMPLATE.format(self.message, self.lines)
