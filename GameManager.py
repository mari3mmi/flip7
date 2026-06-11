from tkinter import messagebox

from Card import Card

class GameManager: 
        def __init__(self, game, display=None):
            self.game = game
            self.display = display

        def displayHand(self, player):
            message = f"Player {self.game.players.index(player)+1} Turn\nHand: {len(player.Hand)} cards"
            if self.display:
                self.display.update_info(message)

        def isFlipSeven(self, hand : list[Card]):
            if self.game.isFlipSeven(hand):
                if self.display:
                    self.display.update_info("You've flipped seven. Congratulations!")
                    messagebox.showinfo("Round Over", "You've flipped seven. Congratulations!")

        def isGameOver(self):
            self.game.isGameOver()
            if self.display:
                message = "Game is Over!\n\n"
                for player in self.game.players:
                    message += f"Player {self.game.players.index(player)+1} Score: {player.Score}\n"
                self.display.update_info(message)
                messagebox.showinfo("Game Over", message)

        def PromptRest(self, player):
            if len(player.Hand) != 0:
                if self.display:
                    choice = self.display.wait_for_action(['Rest', 'Draw'])
                    self.game.PromptRest(player, choice)


        def selectPlayer(self, player, action):
            available_players = [i+1 for i, p in enumerate(self.game.players) 
                            if not (p.Frozen or p.Busted or p.Rested)]
            
            if not available_players:
                return None
            
            if self.display:
                self.display.update_info(f"Player {self.game.players.index(player)+1}'s Turn\nSelect a player to give {action} to.")
                messagebox.showinfo("Action Card", f"You drew an Action Card,\nSelect a player to give {action} to.")
                options = [f"Player {i}" for i in available_players]
                choice = self.display.wait_for_action(options)
                if choice:
                    return self.game.players[int(choice.split()[-1]) - 1]

        def handleDrawnCard(self, card : Card, player):
            action = self.game.handleDrawnCard(card, player)
            match action: 
                case 'Second Chance': 
                    self.game.handleSecondChanceAction(player, card)
                case 'Flip Three': 
                    self.game.handleFlipThreeAction(self.selectPlayer(player, action), card)
                case 'Freeze':
                    self.game.handleFreezeAction(self.selectPlayer(player, action), card)     

        def gameLoop(self): 
            self.game.deck.shuffle()
            while not self.game.Over:  
                for player in self.game.players: 
                    self.displayHand(player)
                    if self.display:
                        self.display.draw_game()
                    
                    if not player.Busted and not player.Frozen and not player.Rested: 
                        self.PromptRest(player)
                        if not player.Rested: 
                            self.handleDrawnCard(self.game.draw(), player)
                        if self.display:
                            self.display.draw_game()
                            self.display.update_info("")
                
                self.game.isRoundOVer()
            
            self.isGameOver()    