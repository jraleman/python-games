"""
Name: Blackjack mini-project.
Author: jraleman
Year: 2013
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# Load card sprite - 949x392pixels (source: jfitz.com)
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
CARD_IMAGES = simplegui.load_image \
("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
CARD_BACK = simplegui.load_image \
("http://commondatastorage.googleapis.com/codeskulptor-assets/CARD_BACK.png")

# Define global variables for cards and stats.
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, \
'T':10, 'J':10, 'Q':10, 'K':10}
IN_PLAY = False
OUTCOME = ""
SCORE = 0

class Card:
    """
    Define class for the cards.
    """
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        """
        Get suit
        """
        return self.suit

    def get_rank(self):
        """
        Get rank.
        """
        return self.rank

    def draw(self, canvas, pos):
        """
        Draw the cards.
        """
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(CARD_IMAGES, card_loc, CARD_SIZE, [pos[0] + \
        CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


class Hand:
    """
    Define class for current values (hand).
    """
    def __init__(self):
        self.hand = []

    # Return a string representation of a hand
    def __str__(self):
        str_hand = ""
        i = 0
        while i in range(0, len(self.hand)):
            str_hand = str_hand + (str(self.hand[i]) + " ")
            i += 1
        return str_hand

    def add_card(self, card):
        """
        Append a card to the hand.
        """
        self.hand.append(card)

    def get_value(self):
        """
        Count aces as 1, if the hand has an ace,
        then add 10 to hand value if it doesn't bust
        """
        value = 0
        ace = False

        for card in self.hand:
            value = value + VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace = True
        if ace and value + 10 <= 21:
            value +=  10
        return value

    def draw(self, canvas, pos):
        """
        Draw a hand on the canvas, use the draw method for cards
        """
        c = 0
        for card in self.hand:
            card.draw(canvas, [pos[0] + CARD_SIZE[0] * c, pos[1]])
            c += 1

class Deck:
    """
    Define class for the deck.
    """
    # Create a Deck object
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.shuffle(self.deck)

    def deal_card(self):
        """
        Deal a card object from the deck
        """
        return self.deck.pop()

    # Return a string representing the deck
    def __str__(self):
        return str(self.deck)

def deal():
    """
    Define event handlers for 'deal' button.
    """
    global OUTCOME, IN_PLAY, player, dealer, deck, SCORE

    OUTCOME = "Hit or Stand?"
    deck = Deck()
    deck.shuffle()

    player, dealer = Hand(), Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
	
    if IN_PLAY:
        SCORE -= 1
    IN_PLAY = True

def hit():
    """
    Define event handlers for 'hit' button.
    """
    global OUTCOME, SCORE, IN_PLAY

    if not IN_PLAY:
        return

    # If the hand is in play, hit the player
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())

    # If busted, assign a message to OUTCOME, update IN_PLAY and SCORE
    if player.get_value() > 21:
        OUTCOME = "Sorry! You busted... New Deal?"
        SCORE -= 1
        IN_PLAY = False

def stand():
    """
    Define event handlers for 'stand' button.
    """
    global OUTCOME, IN_PLAY, SCORE
    # If hand is in play, repeatedly hit dealer until
    # his hand has a value of 17 or more.
    if not IN_PLAY:
        return

    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())

    # Assign a message to OUTCOME, update IN_PLAY and SCORE
    if dealer.get_value() > 21:
        OUTCOME = "The Dealer has busted! New Deal?"
        SCORE += 1
    else:
        if player.get_value() <= dealer.get_value():
            OUTCOME = "The dealer wins... New Deal?"
            SCORE -= 1
        else:
            OUTCOME = "You win! New Deal?"
            SCORE += 1
    IN_PLAY = False

def draw(canvas):
    """
    Draw handler
    """
    canvas.draw_text("Blackjack: The Game", (80, 60), 50, "#8C001A")
    canvas.draw_text("Score: " + str(SCORE), (250, 570), 30, "#FCDFFF")
    canvas.draw_text("Player's Hand: " + str(player.get_value()), \
    (95, 495), 16, "#FFCBA4")
    canvas.draw_text("Player:", (75, 350), 25, "#483C32")
    canvas.draw_text("Dealer:", (75, 130), 25, "#483C32")
    canvas.draw_text(OUTCOME, (125, 290), 25, "#E0FFFF")

    player.draw(canvas, [75, 370])
    dealer.draw(canvas, [75, 150])

    if IN_PLAY:
        canvas.draw_image(CARD_BACK, CARD_BACK_CENTER, CARD_BACK_SIZE, \
        [75 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# Get things rolling
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("#347C17")
frame.add_button("Deal", deal, 150)
frame.add_button("Hit", hit, 150)
frame.add_button("Stand", stand, 150)
frame.set_draw_handler(draw)
deal()
frame.start()
