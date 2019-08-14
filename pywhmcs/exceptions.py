from typing import List, Optional, Union

class WHMCSException(Exception):
    """Base exception class for all internal exceptions."""
    message: str
    whmcs_message: Optional[Union[str, List[str]]] = None

    def __init__(self, message=None, action=None, response=None):
        super().__init__(message or self.__class__.message)
        self.action = action
        self.response = response


class UnknownError(WHMCSException):
    message = 'Unknown error'


class ResourceNotFound(Exception):
    message = 'Resource not found'


class CommandNotFound(WHMCSException):
    message = 'Command not found'
    whmcs_message = message.lower()


class ClientNotFound(WHMCSException, ResourceNotFound):
    message = 'Client not found'
    whmcs_message = message.lower()


class UserAlreadyExists(WHMCSException):
    """Raised when account already exists with specified email address."""
    message = 'A user already exists with that email address'
    whmcs_message = message.lower()


class OrderNotFound(WHMCSException, ResourceNotFound):
    message = 'Order ID not found'
    whmcs_message = [
        message.lower(),
        'Order ID not found or Status not Pending'.lower()
    ]


class PaymentFailed(WHMCSException):
    message = 'Payment attempt failed'
    whmcs_message = message.lower()


class InvalidEmailOrPassword(WHMCSException):
    message = 'Email or Password Invalid'
    whmcs_message = message.lower()


class InvoiceNotFound(WHMCSException, ResourceNotFound):
    message = 'Invoice ID Not Found'
    whmcs_message = message.lower()


class TicketNotFound(WHMCSException, ResourceNotFound):
    message = 'Ticket ID not found'
    whmcs_message = message.lower()


###


class RestrictedIPError(WHMCSException):
    """Raised when attempting to call API from a non-whitelisted IP Address."""
    message = 'Source IP is not white-listed'


class AuthenticationFailed(WHMCSException):
    """"Raised when authentication of a user fails."""
    message = "Authentication failed"


class ResourceNotUnique(WHMCSException):
    """
    Raised when a lookup for a specific resource returns multiple matching
    resources.
    """
    message = "Multiple matching resources found"


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
_code_map = tuple((c.whmcs_message, c) for c in _error_classes if c.whmcs_message)


def from_response(response, action):
    """
    Return an instance of an WHMCSException or subclass
    based on a response.
    """

    content = response.json()

    whmcs_message = content['message'].lower()

    for (msg, exc) in _code_map:
        if (isinstance(msg, list) and whmcs_message in msg
                or whmcs_message == msg):
            cls = exc(action=action, response=response)
            break
    else:
        cls = UnknownError(content['message'], action=action, response=response)

    return cls
