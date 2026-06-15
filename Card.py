import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

class Card:
    """Represents a single playing card."""
    def __init__(self, type, val):
        self.type = type
        self.value = val
        # keep the original PIL image for dynamic transforms (flip/resize)
        pil_img = Image.open(f"{Path(__file__).parent}\\resources\\{self.type}_{str(self.value).replace(' ', '')}.png").resize((40, 80))
        self.pil_image = pil_img
        self.image = ImageTk.PhotoImage(pil_img)

    def __repr__(self):
        # Provides a human-readable string representation of the card
        return f"{self.type} of {self.value}"