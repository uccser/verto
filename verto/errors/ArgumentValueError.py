from verto.errors.Error import Error


class ArgumentValueError(Error):
    '''Exception raised when an argument is not one of the required
    values.

    Attributes:
        tag: tag which was not matched
        argument: the argument that was not found
        value: the value that was not matched
        message: explanation of why error was thrown
    '''

    def __init__(self, tag, argument, value, message):
        super().__init__(message)
        self.tag = tag
        self.argument = argument
        self.value = value
        self.message = message
