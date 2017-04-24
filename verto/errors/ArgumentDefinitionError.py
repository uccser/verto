from verto.errors.Error import Error


class ArgumentDefinitionError(Error):
    '''Exception raised when an argument exists but is not readable.
    The most likely scenario is that an author has used single quotes
    instead of double quotes.

    Attributes:
        argument: the argument that was at error
        message: explanation of why error was thrown
    '''

    def __init__(self, argument, message):
        super().__init__(message)
        self.argument = argument
        self.message = message
