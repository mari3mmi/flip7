import tkinter as tk
from Game import Game
from PIL import Image, ImageTk
from CardGameDisplay import CardGameDisplay
from GameManager import GameManager
import threading


def createGame(num_players):
    game = Game(num_players)
    gameManager = GameManager(game)
    
    # Create display and pass to game
    display = CardGameDisplay(root, game, num_players)
    game.display = display
    
    # Start game loop in separate thread to keep GUI responsive
    game_thread = threading.Thread(target=gameManager.gameLoop, daemon=True)
    game_thread.start()
    
    # Run GUI
    root.mainloop()

if __name__ == "__main__":
    main()