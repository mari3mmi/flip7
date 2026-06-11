import string

from Player import Player
from Deck import Deck
from Card import Card
import math
import tkinter as tk
from tkinter import messagebox
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

class Game:
    def __init__(self, numberOfPlayers):
        self.round = 0
        self.deck = Deck()
        self.Over = False
        self.players = [Player() for i in range(numberOfPlayers)]
        self.playablePlayers = 0

    def draw(self) -> Card: 
        card = self.deck.deal()
        if card == None: 
            self.deck.reset(True)
            self.deck.shuffle()
            self.draw()
        else: 
            return self.deck.deal()

    def handleDrawnCard(self, card : Card, player) -> string:
        logging.info(f"Player {self.players.index(player)+1} drew {card}")
        if (card.type == 'Action'):
           return self.handleActionCard(card)

        elif (card not in player.Hand or card.type == 'Modifier' or card.type == 'Multiplier'):
            player.Hand.append(card)

        elif (card.type == 'Number'):
            self.handleNumberCard(card, player)
        return ''
        
    def handleActionCard(self, card : Card):
        return card.value

    def handleSecondChanceAction(self, player, card):
        player.SecondChance+=1
        player.Hand.append(card)

    def handleFreezeAction(self, chosen, card):
        chosen.Frozen = True
        self.deck.discard.append(card)

    def handleFlipThreeAction(self, chosen, card):
        for x in range(3):
            self.handleDrawnCard(self.draw(), chosen)
            if chosen.Busted: break
            x+=1
        self.deck.discard.append(card)

    def handleNumberCard(self, card : Card, player):
        if (player.SecondChance > 0): 
            player.SecondChance-=1
            self.deck.discard.append(card)
            cardToRemove = next((c for c in player.Hand if (c.type == 'Action' and c.value == 'Second Chance')))
            player.Hand.remove(cardToRemove)
            self.deck.discard.append(cardToRemove)
        else: 
            player.Busted = True
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
            self.deck.discard.append(player.Hand)
            player.reset()
            if player.Score > 199: 
                self.Over = True
        
    def isFlipSeven(self, hand : list[Card]):
        if sum(1 for card in hand if card.type == 'Number') == 7:
            self.calculateScores(True)
            self.round+=1
            return True

    def isRoundOVer(self):
        if (len(self.players) == sum(1 for player in self.players if (player.Busted or player.Frozen or player.Rested))):
            self.calculateScores()
            self.round+=1
    
    def isGameOver(self) -> bool:
        return self.Over

    def PromptRest(self, player, choice):
        player.Rested = choice == 'Rest'


