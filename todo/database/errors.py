class LoginIsUnavailable(Exception):
    """Raised when user passed login is already used."""
    
class ItemDoesNotExist(Exception):
    """Raised when user tries to get item that does not exist"""
  