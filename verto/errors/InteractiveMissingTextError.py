from verto.errors.Error import Error


class InteractiveMissingTextError(Error):
    '''Exception raised when an interactve is missing text.

    Attributes:
        tag: tag which was not matched
        argument: the argument that was not found
    '''

    def __init__(self, tag, argument):
        self.tag = tag
        self.argument = argument
        self.message = '\'text\' is \'true\' but not supplied.'
        super().__init__(self.message)
