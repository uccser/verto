from verto.errors.Error import Error


class ImageCaptionContainsImageError(Error):
    '''Exception raised when a caption includes an image block.

    Attributes:
        tag: tag which was not matched
    '''

    def __init__(self, tag):
        self.tag = tag
        self.message = 'Image caption cannot contain another image.'
        super().__init__(self.message)
