from Game import Game

def main():
    # Your primary program logic goes here
    game = Game(int(input("Enter number of players: ")))
    game.gameLoop()

if __name__ == "__main__":
    main()