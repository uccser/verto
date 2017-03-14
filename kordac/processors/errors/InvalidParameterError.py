from kordac.processors.errors.Error import Error


class InvalidParameterError(Error):
    """Exception raised when an invalid parameter value is found.

    Attributes:
        tag -- tag which was not matched
        block -- block where tag was not matched
        parameter -- the parameter that was not found
        message -- explanation of why error was thrown
    """

    def __init__(self, tag, parameter, message):
        super().__init__(message)
        self.tag = tag
        self.parameter = parameter
        self.message = message
