"""
This module provides a Deck object used to store and manipulate a deck of
cards, as well as a ShuffleStrategy enum for tuning shuffling behavior.
"""

from .card import Card, Suit
from .exceptions import CardDeckSortError, CardDeckShuffleError, CardDeckEmptyDeckError
import random
from enum import Enum


class Deck:
    """
    Stores and manipulates a list of cards to be used as deck.

    :param cards: A list of cards the deck will contain.
    """
    def __init__(self, cards=None):
        if not cards:
            self.cards = []
        else:
            self.cards = []
            for card in cards:
                if isinstance(card, Card):
                    self.cards.append(card)
                else:
                    self.cards.append(Card.deserialize(card))

    def pop(self):
        """ Pull the top card off the deck. """
        try:
            return self.cards.pop(0)
        except IndexError as ind_err:
            raise CardDeckEmptyDeckError(
                "The current deck is empty.") from ind_err

    def shuffle(self, strategy=None):
        """Shuffle the deck.

        :param strategy: ShuffleStrategy to be used for this shuffle.
        """
        if not strategy or strategy == ShuffleStrategy.RANDOM:
            self.__shuffle_random()
        elif strategy == ShuffleStrategy.RIFFLE:
            self.__shuffle_riffle()
        elif strategy == ShuffleStrategy.CUT:
            self.__shuffle_cut()
        else:
            raise CardDeckShuffleError("Invalid shuffle strategy provided")

    def sort(self, suit_ranks=None):
        """Sort the deck.

        :param suit_ranks: The order in which the suits will appear in the
                           sorted deck. Expects a list containing all four
                           suits exactly once.
        """
        if not suit_ranks:
            suit_ranks = [Suit.SPADES, Suit.DIAMONDS, Suit.HEARTS, Suit.CLUBS]
        suit_ranks = suit_ranks[:4]
        if len(suit_ranks) != 4:
            raise CardDeckSortError("suit_ranks must contain all 4 suits.")
        if sorted(suit_ranks) != [
                Suit.SPADES, Suit.DIAMONDS, Suit.HEARTS, Suit.CLUBS
        ]:
            raise CardDeckSortError("suit_ranks must contain all 4 suits.")
        suit_map = {}
        for i in range(4):
            suit_map[suit_ranks[i]] = i * 100

        # Diabling protected access because there is no use-case for a user to
        # call _get_suitsort_value directly on a Card, however it is cleaner
        # leave that method on Card rather than implement it in Deck.
        # pylint: disable=protected-access
        self.cards.sort(key=lambda c: c._get_suitsort_value(suit_map))

    def __shuffle_random(self):
        old_cards = self.cards.copy()
        while self.cards == old_cards:
            random.shuffle(self.cards)

    def __shuffle_riffle(self):
        if len(self.cards) < 10:
            raise CardDeckShuffleError("The deck must contain at least 10"
                                       " cards to perform a riffle.")
        cards_per_hand = len(self.cards) // 2
        hand1 = self.cards[:cards_per_hand]
        hand2 = self.cards[cards_per_hand:]
        new_cards = []
        while len(hand1) > 0 or len(hand2) > 0:
            hand1_drop = random.randint(1, 3)
            hand2_drop = random.randint(1, 3)
            new_cards.extend(hand1[:hand1_drop])
            new_cards.extend(hand2[:hand2_drop])
            del hand1[:hand1_drop]
            del hand2[:hand2_drop]
        self.cards = new_cards

    def __shuffle_cut(self):
        if len(self.cards) < 10:
            raise CardDeckShuffleError("The deck must contain at least 10"
                                       " cards to perform a cut.")
        q1 = len(self.cards) // 3
        q3 = q1 * 2
        cut_point = random.randint(q1, q3)
        new_cards = []
        new_cards.extend(self.cards[cut_point:])
        new_cards.extend(self.cards[:cut_point])
        self.cards = new_cards

    def __str__(self):
        ret = ""
        for card in self.cards:
            ret += str(card)
        return ret

    @classmethod
    def deserialize(cls, string):
        """ Return a Deck from a string representation. """
        chunked = [string[i:i + 2] for i in range(0, len(string), 2)]
        return Deck(cards=chunked)

    @classmethod
    def standard_deck(cls):
        """ Returns an instance of Deck containing a single instance of every
        valid playing card exactly once. This deck will be sorted. """
        suits = "hdsc"
        vals = "23456789TJQKA"
        deck = ""
        for suit in suits:
            for val in vals:
                deck += "%s%s" % (
                    val,
                    suit,
                )
        return Deck.deserialize(deck)


class ShuffleStrategy(Enum):
    """ Enum that can be provided to Deck.shuffle() to modify the shuffling
    method. """
    RANDOM = 1
    RIFFLE = 2
    CUT = 3
