import math
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, Button, Label


class CardGameDisplay:
    def __init__(self, root, game, num_players=4):
        self.root = root
        self.game = game
        self.num_players = num_players
        self.root.title('Flip 7 - Card Game')
        self.root.geometry('1200x900')
        
        self.canvas = Canvas(root, width=1200, height=800, bg='green')
        self.canvas.pack(pady=10)
        
        self.center_x = 600
        self.center_y = 400
        self.radius = 300
        
        # Info panel at bottom
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.info_label = Label(self.info_frame, text='', font=('Arial', 10), justify=tk.LEFT)
        self.info_label.pack(side=tk.LEFT)
        
        self.action_frame = tk.Frame(root)
        self.action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.action_buttons = []
        self.current_player_idx = 0
        self.waiting_for_action = False
        self.player_action = None
        
        # Store image references to prevent garbage collection
        self.image_cache = {}
        self.load_images()
        
        self.draw_game()
    
    def load_images(self):
        """Load and cache card images"""
        try:
            back_image = Image.open("resources/back.png").resize((60, 90))
            self.image_cache['back'] = ImageTk.PhotoImage(back_image)
        except Exception as e:
            print(f"Could not load back.png: {e}")
            self.image_cache['back'] = None
    
    def draw_game(self):
        """Redraw the entire game board"""
        self.canvas.delete('all')
        
        # Draw deck and discard pile in center
        self.draw_deck()
        self.draw_discard()
        
        # Draw player hands in circle
        self.draw_player_hands()
    
    def draw_deck(self):
        """Draw deck pile (left of center)"""
        x = self.center_x - 100
        y = self.center_y
        self.canvas.create_rectangle(x-30, y-40, x+30, y+40, outline='white', width=2)
        
        # Draw deck image if available
        if self.image_cache.get('back'):
            self.canvas.create_image(x, y, image=self.image_cache['back'])
        
        self.canvas.create_text(x, y+20, text='DECK\n(' + str(len(self.game.deck.cards)) + ')', 
                               fill='black', font=('Arial', 10, 'bold'))
    
    def draw_discard(self):
        """Draw discard pile (right of center)"""
        x = self.center_x + 100
        y = self.center_y
        self.canvas.create_rectangle(x-30, y-40, x+30, y+40, 
                                     fill='darkred', outline='white', width=2)
        #if len(self.game.deck.discard) > 0:
            #self.canvas.create_image(x, y, image=self.game.deck.discard[-1].image)
        self.canvas.create_text(x, y+20, text='DISCARD\n(' + str(len(self.game.deck.discard)) + ')', 
                               fill='black', font=('Arial', 10, 'bold'))
    
    def draw_player_hands(self):
        """Draw player positions in a circle"""
        angle_step = 360 / self.num_players
        
        for i in range(self.num_players):
            angle = math.radians(i * angle_step - 90)
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            
            player = self.game.players[i]
            
            # Determine player status color
            if player.Busted:
                color = 'lightcoral'
                status = 'BUSTED'
            elif player.Frozen:
                color = 'lightblue'
                status = 'FROZEN'
            elif player.Rested:
                color = 'lightyellow'
                status = 'RESTING'
            else:
                color = 'lightgreen'
                status = f'Score: {player.Score}'
            
            # Draw player circle
            self.canvas.create_oval(x-50, y-50, x+50, y+50, 
                                   fill=color, outline='black', width=2)
            self.canvas.create_text(x, y-15, text=f'Player {i+1}', 
                                   font=('Arial', 11, 'bold'))
            self.canvas.create_text(x, y+15, text=status, 
                                   font=('Arial', 9))
            
            # Draw hand cards
            hand_y = y + 80
            card_width = 35
            total_width = len(player.Hand) * card_width
            start_x = x - total_width // 2
            
            for j, card in enumerate(player.Hand):
                card_x = start_x + j * card_width
                self.canvas.create_rectangle(card_x, hand_y, card_x+30, hand_y+50, outline='black', width=1)
                self.canvas.create_image(card_x, hand_y, anchor="nw", image=card.image)
                
    
    def update_info(self, text):
        """Update info panel"""
        self.info_label.config(text=text)
        self.root.update()
    
    def clear_action_buttons(self):
        """Clear action buttons"""
        for btn in self.action_buttons:
            btn.destroy()
        self.action_buttons = []
    
    def show_action_buttons(self, options):
        """Show buttons for player actions"""
        self.clear_action_buttons()
        for option in options:
            btn = Button(self.action_frame, text=option, width=15,
                        command=lambda opt=option: self.set_player_action(opt))
            btn.pack(side=tk.LEFT, padx=5)
            self.action_buttons.append(btn)
    
    def set_player_action(self, action):
        """Set the player's chosen action"""
        self.player_action = action
        self.waiting_for_action = False
    
    def wait_for_action(self, options):
        """Wait for player to choose an action"""
        self.waiting_for_action = True
        self.player_action = None
        self.show_action_buttons(options)
        
        while self.waiting_for_action:
            self.root.update()
        
        return self.player_action