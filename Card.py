class Card:
    """Represents a single playing card."""
    def __init__(self, type, val):
        self.type = type
        self.value = val

    def __repr__(self):
        # Provides a human-readable string representation of the card
        return f"{self.type} of {self.value}"