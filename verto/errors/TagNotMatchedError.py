from verto.errors.Error import Error


class TagNotMatchedError(Error):
    '''Exception raised when a custom markdown tag in not matched.

    Attributes:
        tag: tag which was not matched
        block: block where tag was not matched
        message: explanation of why error was thrown
    '''

    def __init__(self, tag, block, message):
        super().__init__(message)
        self.tag = tag
        self.block = block
        self.message = message
