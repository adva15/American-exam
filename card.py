from enum import Enum
import random
from abc import ABC, abstractmethod


class CardSuit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

class CardRank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class AbcCard(ABC):
    @property
    @abstractmethod
    def suit(self):
        pass

    @property
    @abstractmethod
    def rank(self):
        pass

    @abstractmethod
    def get_display_name(self):
        pass


class Card(AbcCard):
    def __init__(self, suit: CardSuit, rank: CardRank):
        self._suit = suit
        self._rank = rank



    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    def get_display_name(self):
        return f"{self.rank.name.capitalize()} of {self.suit.name.capitalize()}"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        if self.rank.value == other.rank.value:
            return self.suit.value < other.suit.value
        return self.rank.value < other.rank.value

    def __gt__(self, other):
        return other < self


    def __hash__(self):
        return hash((self.rank, self.suit))

    def __str__(self):
        return self.get_display_name()

    def __repr__(self):
        return f"Card({self.rank.name}, {self.suit.name})"


class AbcDeck(ABC):
    @property
    @abstractmethod
    def cards(self):
        pass

    @abstractmethod
    def shuffle(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def add_card(self, card):
        pass


class Deck(AbcDeck):
    def __init__(self, shuffle=True):
        self._cards = [Card(s, r) for s in CardSuit for r in CardRank]
        if shuffle:
            random.shuffle(self._cards)


    @property
    def cards(self):
        return self._cards.copy()

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self):
        return self._cards.pop(0) if self._cards else None

    def add_card(self, card):
        if not isinstance(card, Card):
            raise ValueError("Only one card can be.")
        self._cards.append(card)

    def __len__(self): return len(self._cards)

    def __getitem__(self, i): return self._cards[i]

    def __iter__(self): return iter(self._cards)

def max_card(*cards): return max(cards)

def cards_stats(*cards, **kwargs):
    results = []
    if 'max' in kwargs:
        results += sorted(cards, reverse=True)[:kwargs['max']]
    if 'min' in kwargs:
        results += sorted(cards)[:kwargs['min']]
    return results


class DeckCheatingError(Exception):
    pass


if __name__ == "__main__":
    deck = Deck()
    print("Accessing cards directly by index:")
    for i in range(5):
        print(f"Card at index {i}: {deck[i]}")
    print()

    print("Iterating through all cards in the deck:")
    for card in deck:
        print(card)

    card1 = Card(CardSuit.HEARTS, CardRank.ACE)
    card2 = Card(CardSuit.SPADES, CardRank.KING)
    print(card1>card2)
    print(card1 == card2)



