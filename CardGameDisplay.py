import math
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Canvas, Button, Label

# Choose a resampling filter compatible across Pillow versions
try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    try:
        RESAMPLE_FILTER = Image.LANCZOS
    except AttributeError:
        RESAMPLE_FILTER = Image.BICUBIC


class CardGameDisplay:
    def __init__(self, root, game, num_players=4):
        self.root = root
        self.game = game
        self.num_players = num_players
        self.root.title('Flip 7 - Card Game')
        self.root.geometry('1200x900')
        
        # board container so we can overlay a second canvas for animations
        self.board_frame = tk.Frame(root, width=1200, height=800)
        self.board_frame.pack(pady=10)

        self.canvas = Canvas(self.board_frame, width=1200, height=800, bg='green')
        self.canvas.pack()

        # overlay canvas sits above the main canvas; use same bg as main canvas to avoid invalid empty bg
        self.overlay = Canvas(self.board_frame, width=1200, height=800, bg=self.canvas['bg'], bd=0, highlightthickness=0)
        self.overlay.place(x=0, y=0)
        # keep overlay hidden until an animation runs
        self.overlay.place_forget()
        # keep references to overlay-generated images to avoid GC
        self.overlay_image_ref = None
        
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
        self.animation_complete_var = tk.BooleanVar(value=False)
        
        self.draw_game()
    
    def load_images(self):
        """Load and cache card images"""
        try:
            back_image = Image.open(f"{Path(__file__).parent}\\resources\\back.png").resize((60, 90))
            # store both PIL image (for animations) and PhotoImage (for display)
            self.back_pil_image = back_image
            self.image_cache['back'] = ImageTk.PhotoImage(back_image)
        except Exception as e:
            print(f"Could not load back.png: {e}")
            self.back_pil_image = None
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
        # remove previous deck visuals
        self.canvas.delete('deck')
        self.canvas.create_rectangle(x-30, y-40, x+30, y+40, outline='white', width=2, tags=('deck',))

        # Draw deck image if available
        if self.image_cache.get('back'):
            self.canvas.create_image(x, y, image=self.image_cache['back'], tags=('deck',))

        self.canvas.create_text(x, y+20, text='DECK\n(' + str(len(self.game.deck.cards)) + ')', 
                               fill='black', font=('Arial', 10, 'bold'), tags=('deck',))
    
    def draw_discard(self):
        """Draw discard pile (right of center)"""
        x = self.center_x + 100
        y = self.center_y
        # remove previous discard visuals
        self.canvas.delete('discard')
        self.canvas.create_rectangle(x-30, y-40, x+30, y+40, 
                                     fill='darkred', outline='white', width=2, tags=('discard',))
        #if len(self.game.deck.discard) > 0:
            #self.canvas.create_image(x, y, image=self.game.deck.discard[-1].image, tags=('discard',))
        self.canvas.create_text(x, y+20, text='DISCARD\n(' + str(len(self.game.deck.discard)) + ')', 
                               fill='black', font=('Arial', 10, 'bold'), tags=('discard',))
    
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
            
            # Draw player circle (tagged for selective redraw)
            self.canvas.create_oval(x-50, y-50, x+50, y+50, 
                                   fill=color, outline='black', width=2, tags=(f'player_{i}',))
            self.canvas.create_text(x, y-15, text=f'Player {i+1}', 
                                   font=('Arial', 11, 'bold'), tags=(f'player_{i}',))
            self.canvas.create_text(x, y+15, text=status, 
                                   font=('Arial', 9), tags=(f'player_{i}',))
            
            # Draw hand cards
            hand_y = y + 80
            card_width = 35
            total_width = len(player.Hand) * card_width
            start_x = x - total_width // 2
            
            for j, card in enumerate(player.Hand):
                card_x = start_x + j * card_width
                self.canvas.create_rectangle(card_x, hand_y, card_x+30, hand_y+50, outline='black', width=1, tags=(f'player_{i}',))
                self.canvas.create_image(card_x, hand_y, anchor="nw", image=card.image, tags=(f'player_{i}',))
                
    def get_player_position(self, player_index):
        """Return the center position for a player around the table."""
        angle_step = 360 / self.num_players
        angle = math.radians(player_index * angle_step - 90)
        x = self.center_x + self.radius * math.cos(angle)
        y = self.center_y + self.radius * math.sin(angle)
        return x, y

    def get_card_target_coords(self, player_index, card_index):
        """Return the top-left card coordinates for a player's hand slot."""
        player_x, player_y = self.get_player_position(player_index)
        hand_y = player_y + 80
        card_width = 35
        player = self.game.players[player_index]
        total_width = (len(player.Hand) + 1) * card_width
        start_x = player_x - total_width // 2
        return start_x + card_index * card_width, hand_y

    def draw_player_hand(self, player_index):
        """Redraw only a single player's visuals and hand (used for targeted updates)."""
        # remove previous visuals for this player
        self.canvas.delete(f'player_{player_index}')

        angle_step = 360 / self.num_players
        angle = math.radians(player_index * angle_step - 90)
        x = self.center_x + self.radius * math.cos(angle)
        y = self.center_y + self.radius * math.sin(angle)

        player = self.game.players[player_index]

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

        # Draw player circle (tagged for selective redraw)
        self.canvas.create_oval(x-50, y-50, x+50, y+50, 
                               fill=color, outline='black', width=2, tags=(f'player_{player_index}',))
        self.canvas.create_text(x, y-15, text=f'Player {player_index+1}', 
                               font=('Arial', 11, 'bold'), tags=(f'player_{player_index}',))
        self.canvas.create_text(x, y+15, text=status, 
                               font=('Arial', 9), tags=(f'player_{player_index}',))

        # Draw hand cards
        hand_y = y + 80
        card_width = 35
        total_width = len(player.Hand) * card_width
        start_x = x - total_width // 2

        for j, card in enumerate(player.Hand):
            card_x = start_x + j * card_width
            self.canvas.create_rectangle(card_x, hand_y, card_x+30, hand_y+50, outline='black', width=1, tags=(f'player_{player_index}',))
            self.canvas.create_image(card_x, hand_y, anchor="nw", image=card.image, tags=(f'player_{player_index}',))

    def animate_draw_card(self, player_index, card, duration=400, steps=20):
        """Animate a drawn card moving from the deck to the player's hand."""

        deck_x = self.center_x - 100
        deck_y = self.center_y
        start_x = deck_x - 20
        start_y = deck_y - 40
        target_x, target_y = self.get_card_target_coords(player_index, len(self.game.players[player_index].Hand))

        dx = (target_x - start_x) / steps
        dy = (target_y - start_y) / steps

        # use center anchor so scaling keeps animation centered
        orig_w, orig_h = card.pil_image.size
        start_cx = start_x + orig_w / 2
        start_cy = start_y + orig_h / 2
        target_cx = target_x + orig_w / 2
        target_cy = target_y + orig_h / 2

        dx = (target_cx - start_cx) / steps
        dy = (target_cy - start_cy) / steps

        # draw animation on the main canvas so the board remains visible beneath
        imgtk = ImageTk.PhotoImage(card.pil_image)
        # keep a strong ref to avoid GC while animating
        self.canvas_image_ref = imgtk
        anim_id = self.canvas.create_image(start_cx, start_cy, image=imgtk, anchor="center", tags='animation')
        # ensure animation is above other canvas items
        try:
            self.canvas.tag_raise(anim_id)
        except Exception:
            pass
        self.animation_complete_var.set(False)

        def step(frame=0):
            progress = frame / max(1, steps)
            # flip scale: 1 -> 0 -> 1 using cosine
            flip_scale = abs(math.cos(progress * math.pi))
            new_w = max(1, int(orig_w * flip_scale))
            # swap from back to face at mid-flip (progress >= 0.5)
            current_image = card.pil_image if progress >= 0.5 else self.back_pil_image
            # resize frame image for flip effect
            if new_w != orig_w:
                resized = current_image.resize((new_w, orig_h), RESAMPLE_FILTER)
            else:
                resized = current_image
            imgtk = ImageTk.PhotoImage(resized)
            # keep reference to avoid GC
            self.canvas_image_ref = imgtk
            self.canvas.itemconfig(anim_id, image=imgtk)

            if frame >= steps:
                self.canvas.delete('animation')
                # update only the deck/discard and affected player's hand to avoid full redraw flicker
                self.draw_deck()
                self.draw_discard()
                self.draw_player_hand(player_index)
                # clear image ref used during animation
                self.canvas_image_ref = None
                self.animation_complete_var.set(True)
                return

            # move the animation on the main canvas
            self.canvas.move(anim_id, dx, dy)
            self.canvas.update_idletasks()
            self.root.after(int(duration / steps), lambda: step(frame + 1))

        step()
        self.root.wait_variable(self.animation_complete_var)

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