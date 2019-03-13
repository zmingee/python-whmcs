class WHMCSException(Exception, object):
    """Base exception class for all internal exceptions."""
    message = 'Unknown Error'

    def __init__(self, message=None, details=None, action=None):
        super().__init__(message or self.__class__.message)
        self.message = message or self.__class__.message
        self.details = details
        self.action = action

    def __str__(self):
        return f'{self.action} {self.message}'


class UnknownError(WHMCSException):
    message = 'Unknown Error'


class RestrictedIPError(WHMCSException):
    """Raised when attempting to call API from a non-whitelisted IP Address."""
    message = 'Your IP ({0}) is not white-listed'

    def __init__(self, message=None):
        if message is not None:
            message = message.lstrip('Invalid IP ')
        super().__init__(self.message.format(message))


class ClientNotFound(WHMCSException):
    message = 'Client not found'


class UserAlreadyExists(WHMCSException):
    """Raised when account already exists with specified email address."""
    message = 'A user already exists with that email address'

    def __init__(self):
        super().__init__(self.message)


class AuthenticationFailed(WHMCSException):
    """"Raised when authentication of a user fails."""
    message = "Authentication failed"


class ResourceNotUnique(WHMCSException):
    """
    Raised when a lookup for a specific resource returns multiple matching
    resources.
    """
    message = "Multiple matching resources found"


class ResourceNotFound(WHMCSException):
    """Raised when a resource cannot be found"""
    message = "Resource not found"


class ParameterError(WHMCSException):
    """Raised when there is an error with the passed parameters"""
    message = "Error evaluating parameter(s)"


class InvalidEmail(WHMCSException):
    """Raised when Email is invalid"""
    message = 'The email address you entered was not valid'


class InvalidPhone(WHMCSException):
    """Raised when Phone number is invalid"""
    message = 'Invalid telephone phone number'


class MissingCustomField(WHMCSException):
    """Raised when missing a required custom field"""
    message = 'You did not provide required custom field value for'


class DuplicateEmail(WHMCSException):
    """Raised when duplicate email is found"""
    message = 'Duplicate Email Address'


class ClientIDNotFound(WHMCSException):
    """Raised when client ID not found"""
    message = 'Client ID Not Found'


_error_classes = WHMCSException.__subclasses__()
_code_map = dict((c.message, c) for c in _error_classes)


def from_response(response, action):
    """
    Return an instance of an WHMCSException or subclass
    based on a response.
    """
    error_message = response['error']['message']
    cls = _code_map.get(error_message, WHMCSException)

    kwargs = {
        'message': error_message,
        'action': action
    }

    return cls(**kwargs)



