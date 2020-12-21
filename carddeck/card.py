"""
This module provides a Card object to represent individual cards in the deck.
"""

from enum import IntEnum
from .exceptions import CardDeckCardError


class Card:
    """
    An individual Card.

    :param value: The value of the card (as a Value object or a serialized
                  Value)
    :param suit: The suit of the card (as a Suit enum or a serialized Suit)
    """
    def __init__(self, value, suit):
        if isinstance(suit, Suit):
            self.suit = suit
        else:
            self.suit = Suit.from_character(suit)

        if isinstance(value, Value):
            self.value = value
        else:
            self.value = Value.from_character(value)

    @classmethod
    def deserialize(cls, string):
        """
        Takes a string representing a Card and returns a Card object.
        """
        if len(string) != 2:
            raise CardDeckCardError("Invalid card.")
        value = Value(string[0])
        suit = Suit.from_character(string[1])
        return Card(value, suit)

    def get_value(self):
        """
        Returns the value of a Card for use in comparing against other cards
        """
        return int(self.suit) * self.value.get_value()

    def _get_suitsort_value(self, suit_values):
        return suit_values[self.suit] + self.value.get_value()

    def __str__(self):
        return "%s%s" % (
            self.value,
            self.suit,
        )


class Suit(IntEnum):
    """
    The suit of a card.
    """
    SPADES = 1
    DIAMONDS = 2
    HEARTS = 3
    CLUBS = 4

    def __str__(self):
        suit_map = {
            Suit.SPADES: "♠",
            Suit.DIAMONDS: "♦",
            Suit.HEARTS: "♥",
            Suit.CLUBS: "♣"
        }
        return suit_map[self]

    @classmethod
    def from_character(cls, c):
        """
        Takes a string representing a Suit and returns a Suit object.
        """
        suit_map = {
            "♠": Suit.SPADES,
            "S": Suit.SPADES,
            "♦": Suit.DIAMONDS,
            "D": Suit.DIAMONDS,
            "♥": Suit.HEARTS,
            "H": Suit.HEARTS,
            "♣": Suit.CLUBS,
            "C": Suit.CLUBS
        }
        try:
            return suit_map[c.upper()]
        except KeyError as ke:
            raise CardDeckCardError("Invalid Suit.") from ke


class Value:
    """
    The value of a card.

    :param value: The value to contain. Expects an integer or string from 2
                  to 9, or a string containing a character to represent a
                  face card.
    """
    def __init__(self, value):
        self.printable_value = value
        self.value = Value.from_character(value)

    def get_value(self):
        return self.value

    def __str__(self):
        return self.printable_value

    @classmethod
    def from_character(cls, c):
        """
        Takes a string representing a Value and returns a Value object.
        """
        value_map = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        try:
            value = int(c)
            if 2 <= value <= 9:
                return value
        except ValueError:
            pass

        try:
            return value_map[c]
        except KeyError:
            pass

        raise CardDeckCardError("Invalid value.")
