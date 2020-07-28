class Error(Exception):
    """class for other exceptions/errors"""

    def __init__(self, reason="Unknown reason!"):
        self.message = reason
        super().__init__(self.message)

    def __str__(self):
        return self.message


class RateLimitError(Exception):
    """Raised when a ratelimit is reached"""

    def __init__(self, source="unknown source"):
        self.message = f"The {source}API ratelimit was reached!"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidPlayerError(Exception):
    """Raised when an invalid player name or uuid is provided"""

    def __init__(self, cause, player):
        self.message = f"Invalid player name or uuid was provided! ({cause})"
        super().__init__(self.message)

        self.cause = cause
        self.player = player

    def __str__(self):
        return self.message


class NullPlayerError(Exception):
    """Raised when the player endpoint returns null for a player"""

    def __init__(self):
        self.message = f"Player returned was null! (Player hasn't joined Hypixel before!)"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidGuildError(Exception):
    """Raised when an invalid guild name or id is provided"""

    def __init__(self, cause="unknown cause"):
        self.message = f"Invalid guild name or id was provided! ({cause})"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidSkyblockProfileError(Exception):
    """Raised when an invalid skyblock profile is provided."""

    def __init__(self, cause="unknown cause"):
        self.message = f"Invalid skyblock profile id was provided! ({cause})"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class HypixelAPIError(Exception):
    """Raised when the Hypixel API decides to shit itself."""

    def __init__(self, cause="unknown cause"):
        self.message = f"The Hypixel API had a problem ({cause})"
        super().__init__(self.message)

    def __str__(self):
        return self.message
