from game import *


def main():
    player = 0
    if player == 0:
        print("You play as black (B).")
    elif player == 1:
        print("You play as white (W).")

    checkers = Game(player)
    checkers.run()


main()