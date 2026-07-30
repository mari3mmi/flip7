from tkinter import messagebox
from unittest import case
from Card import Card



#User Input Handling
#State Evaluation Popup (ex: Game Over, Round Over, Used Second Chance)
#Update Display (ex: Player's Hand, Player's Status, Deck Size, etc.)
class GameManager:
    def __init__(self, game, display):
        self.game = game
        self.display = display

    def displayHand(self, player):
        message = f"Player {self.game.players.index(player)+1} Turn\nHand: {len(player.Hand)} cards"
        self.display.update_info(message)

    def PromptRest(self, player):
        if len(player.Hand) != 0:
            choice = self.display.wait_for_action(['Rest', 'Draw'])
            self.game.PromptRest(player, choice)

    def handleDrawnCard(self, card : Card, player):
        if card is None:
            return
        self.display.animate_draw_card(self.game.players.index(player), card)   
        value = self.game.handleDrawnCard(card, player)     
        match value:
            case 'Second Chance': 
                self.game.handleSecondChanceAction(player, card)
            case 'Freeze':
                chosen = self.selectPlayer(player, "select player to Freeze: ")
                self.game.handleFreezeAction(chosen, card)
            case 'Flip Three': 
                chosen = self.selectPlayer(player, "select player to Flip Three: ")
                self.game.handleFlipThreeAction(card)
                for x in range(3):
                    self.handleDrawnCard(self.game.draw(), chosen)
                    if chosen.Busted: break
                    x+=1
            case 'Number':
                result = self.game.handleDuplicateNumberCard(card, player)
                if result == 'Second Chance': 
                    self.display.update_info(f"Player {self.game.players.index(player)+1}'s Turn\n You've used a Second Chance card to avoid busting.")
                    messagebox.showinfo("Second Chance", "You've used a Second Chance card to avoid busting.")



    def selectPlayer(self, player, prompt):
        available_players = [i+1 for i, p in enumerate(self.game.players) 
                           if not (p.Frozen or p.Busted or p.Rested)]
        
        if not available_players:
            return None

        self.display.update_info(f"Player {self.game.players.index(player)+1}'s Turn\n{prompt}")
        messagebox.showinfo("Action Card", f"You drew an Action Card,\n{prompt}.")
        options = [f"Player {i}" for i in available_players]
        choice = self.display.wait_for_action(options)
        if choice:
            return self.game.players[int(choice.split()[-1]) - 1]

    def isFlipSeven(self, hand : list[Card]):
        if self.game.isFlipSeven(hand):
            self.display.update_info("You've flipped seven. Congratulations!")
            messagebox.showinfo("Round Over", "You've flipped seven. Congratulations!")

    def isGameOver(self):
        if self.game.Over: 
            message = "Game is Over!\n\n"
            for player in self.game.players:
                message += f"Player {self.game.players.index(player)+1} Score: {player.Score}\n"
            self.display.update_info(message)
            messagebox.showinfo("Game Over", message)

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
                        self.isFlipSeven(player.Hand)
                    
                    if self.display:
                        self.display.draw_game()
                        self.display.update_info("")
            
            self.game.isRoundOVer()
        
        self.isGameOver()

    

         