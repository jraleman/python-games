"""
Name: Memory mini-project.
Author: jraleman
Year: 2013
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# Initialize the global variables for turns, and cards.
count = 0
turns = 0
flipCard = []
listCard = []

# Color of card properties
borderCard = "#E3E4FA"
downCard = "#786D5F"
upCard = "#347C17"
upText = "#FFCBA4"
pairCard = "#54C571"
pairText = "#FFF8DC"

def new_game():
    """
    Helper function to start a game, re-initialize the global variables.
    Create a list of sixteen (16) random cards faced down, and shuffle them.
    """
    global count, turns, flipCard, listCard
    count = 0
    turns = 0
    flipCard = []
    listCard = []
    label.set_text("Turns")
    for i in range(16):
        listCard.append([ i // 2 , downCard, downCard])
        random.shuffle(listCard)

def mouseclick(pos):
    """
    Define event handlers. Checks if there is a match.
    If not, put cards faced down.
    If there is, put both cards faced up.
    Restarts the count to zero (0), to start a new match.
    Increment turns by one (1), to see how many turns the player have taken.
    """
    global count, flipCard, turns

    if count == 2:
        for i in range(len(listCard)):
            if listCard[i][2] != pairText:
                listCard[i][1], listCard[i][2] = downCard, downCard
                count = 0

    for i in range(len(listCard)):
        if pos[0] > (i * 50) and pos[0] < (i * 50 + 50) and \
        (listCard[i][1] == downCard):
            listCard[i][1] = upCard
            listCard[i][2] = upText
            count += 1
            if count % 2 == 1:
                flipCard = listCard[i]
            elif count % 2 == 0:
                if listCard[i][0] == flipCard[0]:
                    listCard[i][1], flipCard[1] = pairCard, pairCard
                    listCard[i][2], flipCard[2] = pairText, pairText
                    count = 0
                turns += 1
                label.set_text("Turns: " + str(turns))

def draw(canvas):
    """
    Draw the cards and the numbers. Cards are logically 50x100 pixels in size.
    Number are located on the card with font size 45.
    """
    for i in range(len(listCard)):
        canvas.draw_polygon([(i * 50, 0), (i * 50 + 50, 0), (i * 50 + 50, 100),\
        (i * 50, 100)], 4, borderCard, listCard[i][1])
        canvas.draw_text(str(listCard[i][0]), (50 * i + 15, 65), 45,\
        listCard[i][2])

# Get things rolling.
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns")
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
new_game()
frame.start()
