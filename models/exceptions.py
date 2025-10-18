class LogException(BaseException):
    """Exception raised for errors in the logging process.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Logging error occurred"):
        super().__init__(message)

