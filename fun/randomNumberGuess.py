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
          f'you can ask if the number is greater than a number or equal to a number')

    secret_number = random.randint(1, 100)

    # print(secret_number)

    count: int = 0

    while True:
        guessed_number = int(input("Guess the number: "))

        if guessed_number == secret_number:
            print(f'Correct number guessed!!!')
            break
        elif guessed_number > secret_number:
            print(f'' + str(guessed_number) + ' is greater than the secret number')
        else:
            print(f'' + str(guessed_number) + ' is lesser than the secret number')

        count += 1
        print(f'' + str(count) + ' times tried')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    player_name = input("What is your name?")
    play_game(player_name)
