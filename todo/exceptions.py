class LoginIsUnavailableError(Exception):
    """Raised when user passed login is already used."""
    
class ItemDoesNotExistError(Exception):
    """Raised when user tries to get item that does not exist"""

class InvalidTokenError(Exception):
    ...

class TokenHasExpiredError(Exception):
    ...

class NoEnoughPriviligesError(Exception):
    ...
    