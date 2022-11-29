# This is a Python script for random number guessing game.
import random


# Press Shift+F10 to execute it
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def play_game(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}. Let\'s play a game of guessing a random number')  # Press Ctrl+F8 to toggle the breakpoint.
    print(f'Aim of the Game: '
          f'The computer has chosen a random number between 1 to 100, your aim is to identify the number'
          f' within 10 turns.')
    print(f'The rules of the game are simple: '
          f'')

    secret_number = random.randint(1, 100)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    player_name = input("What is your name?")
    play_game(player_name)
