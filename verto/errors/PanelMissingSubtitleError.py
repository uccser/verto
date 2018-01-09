from verto.errors.Error import Error


class PanelMissingSubtitleError(Error):
    '''Exception raised when a panel is missing a subtitle.

    Attributes:
        tag: tag which was not matched
        block: block where tag was not matched
        argument: the argument that was not found
    '''

    def __init__(self, tag, argument):
        self.tag = tag
        self.argument = argument
        self.message = '\'subtitle\' is \'True\' but not supplied.'
        super().__init__(self.message)
