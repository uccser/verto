from verto.errors.Error import Error


class PanelMissingTitleError(Error):
    '''Exception raised when a panel is missing a title.

    Attributes:
        tag: tag which was not matched
        block: block where tag was not matched
        argument: the argument that was not found
    '''

    def __init__(self, tag, argument):
        self.tag = tag
        self.argument = argument
        self.message = 'Panel missing title (required).'
        super().__init__(self.message)
