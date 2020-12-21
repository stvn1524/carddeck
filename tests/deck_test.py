"""
Tests related to the Deck class
"""
import pytest
import carddeck

class TestDeck:
    def test_instantiate(self):
        cards = [
            carddeck.Card.deserialize("Qs"),
            "3♠",
            "6c",
            carddeck.Card.deserialize("2D"),
            carddeck.Card.deserialize("Qh")
        ]
        deck = carddeck.Deck(cards=cards)

    def test_deserialize(self):
        str_deck = "2S3S4S5S6S7S8S9STSJSQSKSAS2h3h4h5h6h7h8h9hThJhQhKhAh"
        deck = carddeck.Deck.deserialize(str_deck)

    def test_serialize(self):
        str_deck = "2S3S4S5S6S7S8S9STSJSQSKSAS2h3h4h5h6h7h8h9hThJhQhKhAh"
        deck = carddeck.Deck.deserialize(str_deck)
        assert("2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥" == str(deck))

    def test_standard_deck(self):
        deck = carddeck.Deck.standard_deck()
        assert(str(deck) == "2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥2♦3♦4♦5♦6♦7♦8♦9♦T♦J♦Q♦K♦A♦2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♣3♣4♣5♣6♣7♣8♣9♣T♣J♣Q♣K♣A♣")

    def test_pop(self):
        deck = carddeck.Deck.standard_deck()
        card = deck.pop()
        assert(str(card) == "2♥")

    def test_pop_empty(self):
        with pytest.raises(carddeck.exceptions.CardDeckEmptyDeckError):
            deck = carddeck.Deck()
            card = deck.pop()

    def test_shuffle_random(self):
        deck = carddeck.Deck.standard_deck()
        deck.shuffle()
        assert(str(deck) != "2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥2♦3♦4♦5♦6♦7♦8♦9♦T♦J♦Q♦K♦A♦2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♣3♣4♣5♣6♣7♣8♣9♣T♣J♣Q♣K♣A♣")
        assert(len(str(deck)) == 104)

    def test_shuffle_riffle(self):
        deck = carddeck.Deck.standard_deck()
        deck.shuffle(strategy=carddeck.deck.ShuffleStrategy.RIFFLE)
        assert(str(deck) != "2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥2♦3♦4♦5♦6♦7♦8♦9♦T♦J♦Q♦K♦A♦2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♣3♣4♣5♣6♣7♣8♣9♣T♣J♣Q♣K♣A♣")
        assert(len(str(deck)) == 104)

    def test_shuffle_riffle_not_enough_cards(self):
        with pytest.raises(carddeck.exceptions.CardDeckShuffleError):
            deck = carddeck.Deck.deserialize("2S3S4S5S")
            deck.shuffle(strategy=carddeck.deck.ShuffleStrategy.RIFFLE)

    def test_shuffle_cut(self):
        deck = carddeck.Deck.standard_deck()
        deck.shuffle(strategy=carddeck.deck.ShuffleStrategy.CUT)
        assert(str(deck) != "2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥2♦3♦4♦5♦6♦7♦8♦9♦T♦J♦Q♦K♦A♦2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♣3♣4♣5♣6♣7♣8♣9♣T♣J♣Q♣K♣A♣")
        assert(len(str(deck)) == 104)

    def test_shuffle_cut_not_enough_cards(self):
        with pytest.raises(carddeck.exceptions.CardDeckShuffleError):
            deck = carddeck.Deck.deserialize("2S3S4S5S")
            deck.shuffle(strategy=carddeck.deck.ShuffleStrategy.CUT)

    def test_shuffle_bad_strategy(self):
        with pytest.raises(carddeck.exceptions.CardDeckShuffleError):
            deck = carddeck.Deck.standard_deck()
            deck.shuffle(strategy="Cheese")
    
    def test_sort(self):
        deck = carddeck.Deck.standard_deck()
        Suit = carddeck.card.Suit
        deck.sort(suit_ranks=[Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES, Suit.CLUBS])
        assert(str(deck) == "2♦3♦4♦5♦6♦7♦8♦9♦T♦J♦Q♦K♦A♦2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♣3♣4♣5♣6♣7♣8♣9♣T♣J♣Q♣K♣A♣")

    def test_sort_default_ranks(self):
        deck = carddeck.Deck.standard_deck()
        deck.sort()
        assert(str(deck) == "2♠3♠4♠5♠6♠7♠8♠9♠T♠J♠Q♠K♠A♠2♦3♦4♦5♦6♦7♦8♦9♦T♦J♦Q♦K♦A♦2♥3♥4♥5♥6♥7♥8♥9♥T♥J♥Q♥K♥A♥2♣3♣4♣5♣6♣7♣8♣9♣T♣J♣Q♣K♣A♣")


    def test_sort_not_enough_suits(self):
        with pytest.raises(carddeck.exceptions.CardDeckSortError):
            deck = carddeck.Deck.standard_deck()
            Suit = carddeck.card.Suit
            deck.sort(suit_ranks=[Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES])

    def test_sort_not_all_suits(self):
        with pytest.raises(carddeck.exceptions.CardDeckSortError):
            deck = carddeck.Deck.standard_deck()
            Suit = carddeck.card.Suit
            deck.sort(suit_ranks=[Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES, Suit.SPADES])
