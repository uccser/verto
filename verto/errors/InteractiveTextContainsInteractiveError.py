from verto.errors.Error import Error


class InteractiveTextContainsInteractiveError(Error):
    '''Exception raised when a text includes an interactive block.

    Attributes:
        tag: tag which was not matched
    '''

    def __init__(self, tag):
        self.tag = tag
        self.message = 'Interactive text cannot contain another interactive.'
        super().__init__(self.message)
