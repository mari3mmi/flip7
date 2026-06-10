import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import math

class CardGameDisplay:
    def __init__(self, root, num_players=4):
        self.root = root
        self.canvas = Canvas(root, width=1000, height=1000, bg='green')
        self.canvas.pack()
        
        self.center_x = 500
        self.center_y = 500
        self.radius = 350
        self.num_players = num_players
        
        self.draw_game()
    
    def draw_game(self):
        # Draw deck and discard pile in center
        self.draw_deck()
        self.draw_discard()
        
        # Draw player hands in circle
        self.draw_player_hands()
    
    def draw_deck(self):
        """Draw deck pile (left of center)"""
        x = self.center_x - 80
        y = self.center_y
        self.canvas.create_rectangle(x-30, y-40, x+30, y+40, 
                                     fill='blue', outline='white', width=2)
        self.canvas.create_text(x, y, text='DECK', fill='white', font=('Arial', 12, 'bold'))
    
    def draw_discard(self):
        """Draw discard pile (right of center)"""
        x = self.center_x + 80
        y = self.center_y
        self.canvas.create_rectangle(x-30, y-40, x+30, y+40, 
                                     fill='red', outline='white', width=2)
        self.canvas.create_text(x, y, text='DISCARD', fill='white', font=('Arial', 10, 'bold'))
    
    def draw_player_hands(self):
        """Draw player positions in a circle"""
        angle_step = 360 / self.num_players
        
        for i in range(self.num_players):
            angle = math.radians(i * angle_step - 90)  # Start at top
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            
            # Draw player label circle
            self.canvas.create_oval(x-40, y-40, x+40, y+40, 
                                   fill='yellow', outline='black', width=2)
            self.canvas.create_text(x, y-10, text=f'Player {i+1}', 
                                   font=('Arial', 10, 'bold'))
            
            # Draw hand area (cards would appear here)
            self.canvas.create_rectangle(x-60, y+50, x+60, y+90, 
                                        fill='lightgray', outline='black', width=1)
            draw_cards_in_hand(self, i, [1, 2])  # Pass empty hand for now



# Display actual cards in hand
def draw_cards_in_hand(self, player_num, cards):
    angle = math.radians(player_num * (360/self.num_players) - 90)
    x = self.center_x + self.radius * math.cos(angle)
    y = self.center_y + self.radius * math.sin(angle)
    
    card_width = 40
    total_width = len(cards) * card_width
    start_x = x - total_width // 2
    
    for i, card in enumerate(cards):
        card_x = start_x + i * card_width
        self.canvas.create_rectangle(card_x, y+50, card_x+40, y+90, 
                                    fill='white', outline='black')
        self.canvas.create_text(card_x+20, y+70, text=str(card), font=('Arial', 8))


# Usage
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Flip7 Card Game')
    root.geometry('1000x1000')
    
    display = CardGameDisplay(root, num_players=4)
    root.mainloop()