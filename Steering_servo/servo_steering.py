from microbit import *

pin1.write_analog(90) # reset to straight on start
MAX_ANGLE = 15
MID_ANGLE = 90

def norm(n):
    """
    Normalise an accelerometer reading across an angle.
    Returns an offset angle to apply to the base (90) in
    whichever direction it is steering.
    """
    n = abs(n)
    if n < 100:
        a = 0 # don't want too much jitter
    else:
        p = n / 1024 # percentage of total angle
        a = int(MAX_ANGLE * p)
    return a

while True:
    x = accelerometer.get_x()
    off = norm(x)
    angle = MID_ANGLE + (off if x < 0 else (-1 * off))
    pin1.write_analog(angle)
    #print(angle)
    sleep(50)