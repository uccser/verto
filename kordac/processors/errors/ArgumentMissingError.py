from kordac.processors.errors.Error import Error


class ArgumentMissingError(Error):
    """Exception raised when a custom markdown tag in not matched.

    Attributes:
        tag -- tag which was not matched
        block -- block where tag was not matched
        argument -- the argument that was not found
        message -- explanation of why error was thrown
    """

    def __init__(self, tag, argument, message):
        super().__init__(message)
        self.tag = tag
        self.argument = argument
        self.message = message
