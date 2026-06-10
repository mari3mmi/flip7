import random
import math
class Card:
    """Represents a single playing card."""
    def __init__(self, type, val):
        self.type = type
        self.value = val

    def __repr__(self):
        # Provides a human-readable string representation of the card
        return f"{self.type} of {self.value}"


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
    

class Player:
    def __init__(self):
        self.Score = 0
        self.SecondChance = 0
        self.Hand : Card = []
        self.Busted = False
        self.Rested = False
        self.Frozen = False
    
    def reset(self):
        self.SecondChance = 0
        self.Hand : Card = []
        self.Busted = False
        self.Rested = False
        self.Frozen = False

class Game:
    def __init__(self, numberOfPlayers):
        self.round = 0
        self.deck = Deck()
        self.Over = False
        self.players = [Player() for i in range(numberOfPlayers)]
        self.playablePlayers = 0

    def flipSeven(self, hand : list[Card]):
        if sum(1 for card in hand if card.type == 'Number') == 7:
            return True


    def draw(self) -> Card: 
        card = self.deck.deal()
        if card == None: 
            self.deck.reset(True)
            self.deck.shuffle()
            self.draw()
        else: 
            return card

    def handleDrawnCard(self, card : Card, player):
        print("Drawn Card:")
        print(card) 
        if (card.type == 'Action'):
            if (card.value == 'Freeze'): 
                chosen = self.players[int(input("select player to Freeze: "))-1]
                while chosen.Frozen == 'True': 
                    print("Player is already Frozen. Please select another player.")
                    chosen = self.players[int(input("select player to Freeze: "))-1]
                chosen.Frozen = True
                self.deck.discard.append(card)
            if (card.value == 'Second Chance'): 
                player.SecondChance+=1
                player.Hand.append(card)
            if (card.value == 'Flip Three'): 
                chosen = self.players[int(input("select player to Flip Three: "))-1]
                for x in range(3):
                    self.handleDrawnCard(self.draw(), chosen)
                    if chosen.Busted: break
                    x+=1
                self.deck.discard.append(card)

        elif (card not in player.Hand or card.type == 'Modifier' or card.type == 'Multiplier'):
            player.Hand.append(card)

        elif (card.type == 'Number'):
            if (player.SecondChance > 0): 
                print("Lucky you! You've used your Second Chance.")
                player.SecondChance-=1
                self.deck.discard.append(card)
                cardToRemove = next((c for c in player.Hand if (c.type == 'Action' and c.value == 'Second Chance')))
                player.Hand.remove(cardToRemove)
                self.deck.discard.append(cardToRemove)
            else: 
                player.Busted = True
                print("You Busted. Oh No!")
                self.deck.discard.append(card)
                self.deck.discard.append(player.Hand)
                player.Hand = []
    

    def calculateScores(self, flippedSeven = False): 
        #TODO: Optimize to avoid cycling through each time. Sort the HAND.
        for player in self.players: 
            if not player.Busted:
                player.Score +=  sum(card.value for card in player.Hand if card.type == 'Number')
                player.Score *= math.prod(card.value for card in player.Hand if card.type == 'Multiplier')
                player.Score +=  sum(card.value for card in player.Hand if card.type == 'Modifier')
                if flippedSeven: 
                    player.Score += 15
            print(f"Player {self.players.index(player)+1} Score: {player.Score}")
            self.deck.discard.append(player.Hand)
            player.reset()
            if player.Score > 199: 
                self.Over = True
        
    def gameLoop(self): 
        #TODO: differentiate round ending and game ending for score
        self.deck.shuffle()
        while not self.Over:  
            for player in self.players: 
                print("============================================")
                print(f"Player's Turn: {self.players.index(player)+1}")
                print("Your Hand:")
                print(player.Hand)
                if not player.Busted and not player.Frozen and not player.Rested: 
                    if len(player.Hand) != 0:
                        player.Rested = input("Would you like to rest your hand: (True of False)").upper() == "TRUE"
                    if not player.Rested: 
                        self.handleDrawnCard(self.draw(), player)
                        if (self.flipSeven(player.Hand)): 
                            print("You've flipped seven. Congratulations!")
                            self.calculateScores(True)
                            self.round+=1
                print("============================================")
            if (len(self.players) == sum(1 for player in self.players if (player.Busted or player.Frozen or player.Rested))):
                self.calculateScores()
                self.round+=1
        if self.Over:
            print("Game is Over.")
            for player in self.players:
                print(f"Player {self.players.index(player)+1} Score: {player.Score}")



def main():
    # Your primary program logic goes here
    game = Game(int(input("Enter number of players: ")))
    game.gameLoop()

if __name__ == "__main__":
    main()