from verto.errors.Error import Error


class HtmlParseError(Error):
    '''Exception raised when parsing HTML text and an
    error is found.

    Attributes:
        line_num: The line number the error occurred on
        offset: The position in the line the error occurred
        message: explanation of why error was thrown
    '''

    def __init__(self, line_num, offset, message):
        super().__init__(message)
        self.line_num = line_num
        self.offset = offset
        self.message = message
