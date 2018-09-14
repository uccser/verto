from verto.errors.Error import Error


class BlockquoteMissingFooterError(Error):
    '''Exception raised when a blockquote is missing a footer when argument is given.

    Attributes:
        tag: tag which was not matched
        block: block where tag was not matched
        argument: the argument that was not found
    '''

    def __init__(self, tag, argument):
        self.tag = tag
        self.argument = argument
        self.message = '\'footer\' is \'true\' but not supplied.'
        super().__init__(self.message)
