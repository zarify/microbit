from microbit import *

bottom = pin8
left = pin12
right = pin16

fwd = [110, 40] # right, left
bck = [65, 85] # right, left
retract = 65
extend = 90

def shuffle():
    bottom.write_analog(extend)
    sleep(200)
    right.write_analog(fwd[0])
    left.write_analog(fwd[1])
    sleep(300)
    bottom.write_analog(retract)
    sleep(200)
    right.write_analog(bck[0])
    left.write_analog(bck[1])
    sleep(300)

def neutral():
    bottom.write_analog(extend)
    sleep(200)
    right.write_analog(fwd[0])
    left.write_analog(fwd[1])
    sleep(200)

neutral()

while True:
    if button_a.was_pressed():
        sleep(1000) # give me enough time to move away
        shuffle()
        shuffle()
        shuffle()