from Card import Card
class Player:
    def __init__(self):
        self.Score = 0
        self.SecondChance = 0
        self.Hand : list[Card] = []
        self.Busted = False
        self.Rested = False
        self.Frozen = False
    
    def reset(self):
        self.SecondChance = 0
        self.Hand : list[Card] = []
        self.Busted = False
        self.Rested = False
        self.Frozen = False