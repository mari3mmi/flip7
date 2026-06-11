from Player import Player
from Deck import Deck
from Card import Card
import math
import tkinter as tk
from tkinter import messagebox


class Game:
    def __init__(self, numberOfPlayers, display=None):
        self.round = 0
        self.deck = Deck()
        self.Over = False
        self.players = [Player() for i in range(numberOfPlayers)]
        self.playablePlayers = 0
        self.display = display

    def draw(self) -> Card: 
        if len(self.deck) == 0: 
            self.deck.reset(True)
            self.deck.shuffle()
            self.draw()
        else: 
            return self.deck.deal()

    def selectPlayer(self, player, prompt):
        available_players = [i+1 for i, p in enumerate(self.players) 
                           if not (p.Frozen or p.Busted or p.Rested)]
        
        if not available_players:
            return None
        
        if self.display:
            self.display.update_info(f"Player {self.players.index(player)+1}'s Turn\n{prompt}")
            messagebox.showinfo("Action Card", f"You drew an Action Card,\n{prompt}.")
            options = [f"Player {i}" for i in available_players]
            choice = self.display.wait_for_action(options)
            if choice:
                return self.players[int(choice.split()[-1]) - 1]
        else:
            chosen = self.players[int(input(prompt))-1]
            while chosen.Frozen or chosen.Busted or chosen.Rested:
                print("Player is already out. Please select another player.")
                chosen = self.players[int(input(prompt))-1]
            return chosen

    def handleDrawnCard(self, card : Card, player):
        print("Drawn Card:")
        print(card) 
        if (card.type == 'Action'):
            self.handleActionCard(card, player)

        elif (card not in player.Hand or card.type == 'Modifier' or card.type == 'Multiplier'):
            player.Hand.append(card)

        elif (card.type == 'Number'):
            self.handleNumberCard(card, player)
        
    def handleActionCard(self, card : Card, player):
        match card.value:
            case 'Second Chance': 
                player.SecondChance+=1
                player.Hand.append(card)
            case 'Freeze':
                self.handleFreezeAction(player, card)
            case 'Flip Three': 
                self.handleFlipThreeAction(player, card)

    def handleFreezeAction(self, player, card):
        chosen = self.selectPlayer(player, "select player to Freeze: ")
        chosen.Frozen = True
        self.deck.discard.append(card)

    def handleFlipThreeAction(self, player, card):
        chosen = self.selectPlayer(player, "select player to Flip Three: ")
        for x in range(3):
            self.handleDrawnCard(self.draw(), chosen)
            if chosen.Busted: break
            x+=1
        self.deck.discard.append(card)

    def handleNumberCard(self, card : Card, player):
        if (player.SecondChance > 0): 
            if self.display:
                self.display.update_info(f"Player {self.players.index(player)+1}'s Turn\n You've used a Second Chance card to avoid busting.")
                messagebox.showinfo("Second Chance", "You've used a Second Chance card to avoid busting.")
            else:
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
        
    def isFlipSeven(self, hand : list[Card]):
        if sum(1 for card in hand if card.type == 'Number') == 7:
            if self.display:
                self.display.update_info("You've flipped seven. Congratulations!")
                messagebox.showinfo("Round Over", "You've flipped seven. Congratulations!")
            else:
                print("You've flipped seven. Congratulations!")
            self.calculateScores(True)
            self.round+=1

    def isRoundOVer(self):
        if (len(self.players) == sum(1 for player in self.players if (player.Busted or player.Frozen or player.Rested))):
            self.calculateScores()
            self.round+=1
    
    def isGameOver(self):
        if self.Over: 
            message = "Game is Over!\n\n"
            for player in self.players:
                message += f"Player {self.players.index(player)+1} Score: {player.Score}\n"
            
            if self.display:
                self.display.update_info(message)
                messagebox.showinfo("Game Over", message)
            else:
                print("Game is Over.")
                for player in self.players:
                    print(f"Player {self.players.index(player)+1} Score: {player.Score}")

    def displayHand(self, player):
        message = f"Player {self.players.index(player)+1} Turn\nHand: {len(player.Hand)} cards"
        if self.display:
            self.display.update_info(message)
        else:
            print("============================================")
            print(f"Player's Turn: {self.players.index(player)+1}")
            print("Your Hand:")
            print(player.Hand)

    def PromptRest(self, player):
        if len(player.Hand) != 0:
            if self.display:
                choice = self.display.wait_for_action(['Rest', 'Draw'])
                player.Rested = choice == 'Rest'
            else:
                player.Rested = input("Would you like to rest your hand: (True or False)").upper() == "TRUE"

    def gameLoop(self): 
        self.deck.shuffle()
        while not self.Over:  
            for player in self.players: 
                self.displayHand(player)
                if self.display:
                    self.display.draw_game()
                
                if not player.Busted and not player.Frozen and not player.Rested: 
                    self.PromptRest(player)
                    if not player.Rested: 
                        self.handleDrawnCard(self.draw(), player)
                        self.isFlipSeven(player.Hand)
                    
                    if self.display:
                        self.display.draw_game()
                        self.display.update_info("")
            
            self.isRoundOVer()
        
        self.isGameOver()


