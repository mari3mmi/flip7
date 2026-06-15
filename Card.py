import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

class Card:
    """Represents a single playing card."""
    def __init__(self, type, val):
        self.type = type
        self.value = val
        self.image = ImageTk.PhotoImage(Image.open(f"{Path(__file__).parent}\\resources\\{self.type}_{str(self.value).replace(' ', '')}.png").resize((40, 80)))

    def __repr__(self):
        # Provides a human-readable string representation of the card
        return f"{self.type} of {self.value}"