import tkinter as tk
from tkinter import simpledialog
from Game import Game
from CardGameDisplay import CardGameDisplay
from GameManager import GameManager
import threading

# Main script to run the game with GUI
if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    num_players = simpledialog.askinteger(
        "Players",
        "Enter number of players (2-5):",
        parent=root,
        minvalue=2,
        maxvalue=5,
    )
    if num_players is None:
        num_players = 4

    root.deiconify()

    game = Game(num_players)

    # Create display and pass to game
    display = CardGameDisplay(root, game, num_players)
    game.display = display
    GameManagerInstance = GameManager(game, display)

    # Start game loop in separate thread to keep GUI responsive
    game_thread = threading.Thread(target=GameManagerInstance.gameLoop, daemon=True)
    game_thread.start()

    # Run GUI
    root.mainloop()