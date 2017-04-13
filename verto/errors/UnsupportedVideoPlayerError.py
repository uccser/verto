from verto.errors.Error import Error


class UnsupportedVideoPlayerError(Error):
    '''Exception raised when video player is not recognised

    Attributes:
        block: block where tag was not matched
        url: original url
        message: explanation of why error was thrown
    '''

    def __init__(self, block, url, message):
        super().__init__(message)
        self.block = block
        self.url = url
        self.message = message
