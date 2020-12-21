"""
Card Tests.
"""
import pytest
import carddeck

class TestCard:
    def test_instantiate(self):
        value = carddeck.card.Value("T")
        suit = carddeck.card.Suit.SPADES
        card = carddeck.Card(value, suit)

    def test_instantiate_strings(self):
        value = 9
        suit = "♠"
        card = carddeck.Card(value, suit)

    def test_instantiate_bad_suit(self):
        with pytest.raises(carddeck.exceptions.CardDeckCardError):
            value = carddeck.card.Value("Q")
            suit = "bad"
            card = carddeck.Card(value, suit)

    def test_instantiate_bad_value(self):
        with pytest.raises(carddeck.exceptions.CardDeckCardError):
            value = carddeck.card.Value("1")
            suit = carddeck.card.Suit.HEARTS
            card = carddeck.Card(value, suit)

    def test_deserialize(self):
        card = carddeck.Card.deserialize("Q♠")

    def test_deserialize_bad_suit(self):
        with pytest.raises(carddeck.exceptions.CardDeckCardError):
            card  = carddeck.Card.deserialize("5Z")

    def test_deserialize_bad_value(self):
        with pytest.raises(carddeck.exceptions.CardDeckCardError):
            card  = carddeck.Card.deserialize("Z♠")

    def test_deserialize_bad_strlen(self):
        with pytest.raises(carddeck.exceptions.CardDeckCardError):
            card  = carddeck.Card.deserialize("Hello")

    def test_get_value(self):
        card = carddeck.Card.deserialize("QS")
        assert(card.get_value() == 12)

    def test_get_suitsort_value(self):
        card = carddeck.Card.deserialize("3C")
        suitsort_map = {
            carddeck.card.Suit.CLUBS: 100
        }
        assert(card._get_suitsort_value(suitsort_map) == 103)

    def test_to_string(self):
        card = carddeck.Card.deserialize("8C")
        assert(str(card) == "8♣")
