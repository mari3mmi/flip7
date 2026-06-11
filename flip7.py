import tkinter as tk
from Game import Game
from CardGameDisplay import CardGameDisplay
import threading

# Main script to run the game with GUI
if __name__ == '__main__':
    root = tk.Tk()
    
    # Create game with 4 players
    num_players = int(input("Enter number of players (2-5): "))
    game = Game(num_players)
    
    # Create display and pass to game
    display = CardGameDisplay(root, game, num_players)
    game.display = display
    
    # Start game loop in separate thread to keep GUI responsive
    game_thread = threading.Thread(target=game.gameLoop, daemon=True)
    game_thread.start()
    
    # Run GUI
    root.mainloop()