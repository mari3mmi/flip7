import tkinter as tk
from Game import Game
from PIL import Image, ImageTk
from CardGameDisplay import CardGameDisplay


def createGame(num_players):
    game = Game(num_players)
    game.gameLoop()


def main():
    # Your primary program logic goes here
    #game = Game(int(input("Enter number of players: ")))
    #game.gameLoop()

    #img = Image.open("flip7\\resources\\back.png")
    #photo = ImageTk.PhotoImage(img)
    
    # ttk.Label(frm, image=photo).grid(column=0, row=0)
    number_of_players = int(input("Enter number of players: "))
    root = tk.Tk()
    root.title('Flip7 Card Game')
    root.geometry('1000x1000')
    
    display = CardGameDisplay(root, number_of_players)
    root.mainloop()

if __name__ == "__main__":
    main()