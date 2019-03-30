from microbit import *
import neopixel
import music

np = neopixel.NeoPixel(pin0, 1)
np.clear()

threshold = -100
running = False
elevated = False
finished = False
from_time = 0
score_time = 0

def started():
    np[0] = (0, 0, 100)
    np.show()

def start_game():
    global from_time
    from_time = running_time()
    np[0] = (0, 100, 0)
    np.show()

def end_game():
    global from_time, score_time
    score_time = round((running_time() - from_time) / 1000, 2)
    np[0] = (100, 0, 0)
    np.show()
    music.play(music.DADADADUM, pin=pin1)

def report_time():
    global score_time
    display.scroll(str(score_time) + " s")

while True:
    a = button_a.was_pressed()
    b = button_b.was_pressed()
    
    if not running and a: # start new game
        started()
        running = True
        elevated = False
    elif finished and b: # report last score
        report_time()
    elif finished and a and b: # reset game
        running = False
        finished = False
        elevated = False
        from_time = 0
        score_time = 0

    y = accelerometer.get_y()
    
    if not elevated and running:
        if y > threshold:
            elevated = True
            start_game()
    elif elevated and running:
        if y <= threshold:
            elevated = False
            running = False
            finished = True
            end_game()
    
    sleep(50)