from verto.errors.Error import Error


class ArgumentMissingError(Error):
    '''Exception raised a required or dependent argument is not found.

    Attributes:
        tag: tag which was not matched
        block: block where tag was not matched
        argument: the argument that was not found
        message: explanation of why error was thrown
    '''

    def __init__(self, tag, argument, message):
        super().__init__(message)
        self.tag = tag
        self.argument = argument
        self.message = message
