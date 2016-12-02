"""
Name: Stopwatch mini-project.
Author: jraleman
Year: 2013
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global variables for timer, counter, and score.
timer = 0
minutes = 0
tens_second = 0
ones_second = 0
tenths_second = 0
counter = 0
success = 0
attempts = 0
score = 0

def format(t):
    """
    Converts time in tenths of a second, into formatted string 00:00.00
    """
    global minutes, tens_second, ones_second, tenths_second

    minutes = counter // 600
    tens_second = (counter // 100) % 6
    ones_second = (counter // 10) % 10
    tenths_second = counter % 10
    return str(minutes) + ":" + str(tens_second) + str(ones_second) + \
    "." + str(tenths_second)

def start_timer():
    """
    Start the timer of the stopwatch.
    """
    timer.start()

def stop_timer():
    """
    Stop the time, increase attempts by one (1), and if the tenths of a second
    is equal to zero (0), the player gets a point.
    """
    global attempts, success, tenths_second

    if timer.is_running():
        timer.stop()
        attempts += 1
        if (tenths_second) == 0:
            success += 1

def reset_timer():
    """
    Set the counter, attempts, and success variables to zero (0),
    and stops the timer.
    """
    global counter, attempts, success

    counter = 0
    attempts = 0
    success = 0
    timer.stop()

def time_handler():
    """
    Event handler for timer with 0.1 sec increase interval
    """
    global counter

    counter += 1

def draw(canvas):
    """
    Draw handler, create the timer and score text,
    and put them in the screen, in a specific position.
    """
    global success
    global attempts

    score = str(success) + " out of " + str(attempts)
    canvas.draw_text(format(timer), [110,120], 75, "#FFF8C6")
    canvas.draw_text(score, [290,20], 20, "#FFF5EE")

# Create timer.
timer = simplegui.create_timer(100, time_handler)

# Get things rolling.
frame = simplegui.create_frame("Stopwatch: The Game", 400, 200)
frame.set_canvas_background("#98AFC7")
frame.set_draw_handler(draw)
frame.add_button("Start", start_timer, 115)
frame.add_button("Stop", stop_timer, 115)
frame.add_button("Reset", reset_timer, 115)
frame.start()
