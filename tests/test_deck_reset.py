import os
import sys
import tkinter as tk
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Deck import Deck
from Card import Card


class DeckResetTests(unittest.TestCase):
    def test_reset_from_discard_returns_cards_not_hands(self):
        root = tk.Tk()
        root.withdraw()
        try:
            deck = Deck()
            hand = [Card('Number', 7)]
            deck.discard.extend(hand)
            deck.cards = []

            deck.reset(useDiscard=True)

            self.assertTrue(deck.cards)
            self.assertIsInstance(deck.cards[0], Card)
            self.assertNotIsInstance(deck.cards[0], list)
        finally:
            root.destroy()


if __name__ == '__main__':
    unittest.main()
