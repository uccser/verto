from verto.errors.Error import Error


class NoSourceLinkError(Error):
    '''Exception raised when no source link is found for a video

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
