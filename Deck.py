import random
from Card import Card


class Deck:
    """Represents a standard deck of playing cards."""
    def __init__(self):
        self.types = ['Number', 'Action', 'Modifier', 'Multiplier']
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.modifiers  = [2,4,6,8,10]
        self.multiplier = [2]
        self.actions = ['Freeze', 'Flip Three', 'Second Chance']
        self.cards : Card = []
        self.discard : Card = []
        self.reset()

    def reset(self, useDiscard = False):
        """Populates the deck with a fresh set of cards."""
        if useDiscard: 
            self.cards = self.discard
            return
        else: 
            self.discard = []
            self.cards = []
            for val in self.actions:
                self.cards.extend([Card('Action', val)] * 3) 
            for val in self.numbers: 
                self.cards.extend([Card('Number', val)] * val)
            self.cards.extend([Card('Modifier', val) for val in self.modifiers]) 
            self.cards.extend([Card('Multiplier', val) for val in self.multiplier])
            return


    def shuffle(self):
        """Randomizes the order of the remaining cards in the deck."""
        random.shuffle(self.cards)

    def deal(self):
        """Removes and returns the top card from the deck. Returns None if empty."""
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

    def __len__(self):
        """Allows calling len() directly on the deck object."""
        return len(self.cards)

    def __print__(self):
        """Allows calling len() directly on the deck object."""
        for card in self.cards: 
            print(card)

    def __repr__(self):
        return f"Deck({len(self.cards)} cards remaining)"