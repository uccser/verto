from verto.errors.Error import Error


class ImageMissingCaptionError(Error):
    '''Exception raised when an image is missing a subtitle.

    Attributes:
        tag: tag which was not matched
        argument: the argument that was not found
    '''

    def __init__(self, tag, argument):
        self.tag = tag
        self.argument = argument
        self.message = '\'caption\' is \'true\' but not supplied.'
        super().__init__(self.message)
