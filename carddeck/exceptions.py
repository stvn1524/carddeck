"""
Exceptions thrown by the carddeck module.
"""


class CardDeckCardError(ValueError):
    """Invalid suit or value provided for card."""


class CardDeckSortError(ValueError):
    """An error occured while trying to sort the deck."""


class CardDeckShuffleError(ValueError):
    """An error occured while trying to shuffle the deck."""


class CardDeckEmptyDeckError(IndexError):
    """The deck was empty when an action was attempted."""
