
class Error(Exception):
    """base class for other exceptions"""
    pass


class RateLimitError(Error):
    """Raised when a api ratelimit is reached with the provided key"""
    pass


class InvalidPlayerError(Error):
    """Raised when an invalid player name or uuid is provided"""
    pass
