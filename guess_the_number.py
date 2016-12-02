"""
Name: Guess the Number mini-project.
Author: jraleman
Year: 2013
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# Global variables for the answer and the number of guesses.
ANSWER = 0
GUESSES = 7

def new_game(low, high):
    """
    Helper function to start and restart the game.
    """
    global ANSWER, GUESSES

    ANSWER = random.randrange(low, high)
    if (GUESSES > 0):
        print "Guess a number from", low, "to", high
        print "Try to guess the number! You have", GUESSES, "guesses."

def input_guess(guess):
    """
    Main game logic goes here.
    """
    global GUESSES

    GUESSES -= 1
    number_guess = int(guess)

    # When the answer and the guess are the same, the player wins.
    if number_guess == ANSWER:
        print "Your guess:", guess, "is correct! Congratulations! :D"

    # Indicate the player if the ANSWER is lower or higher.
    elif GUESSES > 0:
        print "Your guess was:", guess
        if number_guess > ANSWER:
            print "Try guessing a LOWER number!"
        if number_guess < ANSWER:
            print "Try guessing a HIGHER number!"
        print "Guesses remaining:", GUESSES

    # Game over condition, shows the ANSWER.
    else:
        print "Game over! You ran out of guesses. Why don't you try again?"
        print "The answer was:", ANSWER

# Get things rolling.
new_game(0, 100)
while(GUESSES):
    input_guess(raw_input("Guess: "))
