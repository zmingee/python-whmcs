class WHMCSException(Exception):
    """Base exception class for all internal exceptions."""
    message = 'Unknown Error'

    def __init__(self, message=None, details=None):
        super().__init__(message or self.__class__.message)
        self.message = message or self.__class__.message
        self.details = details

    def __str__(self):
        return f'{self.message}'


class UnknownError(WHMCSException):
    message = 'Unknown Error'


class ClientNotFound(WHMCSException):
    message = 'Client not found'
