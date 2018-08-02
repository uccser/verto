from verto.errors.Error import Error


class CustomArgumentRulesError(Error):
    '''Exception raised when custom argument rules refer to a processors
    that does not exist.

    Attributes:
        tag: tag which was not matched
        argument: the argument that was not found
        value: the value that was not matched
        message: explanation of why error was thrown
    '''

    def __init__(self, argument, message):
        super().__init__(message)
        self.argument = argument
