from microbit import *
import radio
import neopixel

np = neopixel.NeoPixel(pin0, 1)

radio.config(channel=50)

bottom = pin8
left = pin12
right = pin16

fwd = [110, 40] # right, left
bck = [65, 85] # right, left
retract = 65
extend = 90

def shuffle(direction):
    if direction == 1:
        f = [fwd[0], fwd[1]]
        b = [bck[0], bck[1]]
    else:
        f = [fwd[1], fwd[0]]
        b = [bck[1], bck[1]]
    bottom.write_analog(extend)
    sleep(150)
    right.write_analog(f[0])
    left.write_analog(f[1])
    sleep(200)
    bottom.write_analog(retract)
    sleep(150)
    right.write_analog(b[0])
    left.write_analog(b[1])
    sleep(200)

def turn(direction):
    bottom.write_analog(extend)
    sleep(150)
    if direction == 1: # left
        left.write_analog(bck[1])
        right.write_analog(fwd[0])
        sleep(200)
        bottom.write_analog(retract)
        sleep(150)
        left.write_analog(fwd[1])
        right.write_analog(bck[0])
    else:   # right
        left.write_analog(fwd[1])
        right.write_analog(bck[0])
        sleep(200)
        bottom.write_analog(retract)
        sleep(150)
        left.write_analog(bck[1])
        right.write_analog(fwd[0])
    sleep(200)

def neutral():
    bottom.write_analog(extend)
    sleep(200)
    right.write_analog(fwd[0])
    left.write_analog(fwd[1])
    sleep(200)

neutral()

listening = False
display.show(Image.NO)

def toggle_radio():
    global listening
    if listening:
        listening = False
        display.show(Image.NO)
        radio.off()
    else:
        listening = True
        display.show(Image("99900:00090:99009:00909:90909"))
        radio.on()

while True:
    if button_a.was_pressed():
        toggle_radio()

    if listening:
        r = radio.receive()
        if not r:
            continue
        if r == "forward":
            shuffle(1)
        elif r == "back":
            shuffle(0)
        elif r == "elevate":
            neutral()
        elif r == "left":
            turn(1)
        elif r == "right":
            turn(0)
        elif r.startswith("flash "):
            colours = r.split(" ")
            try:
                r,g,b = map(int, colours[1:])
                np[0] = (r,g,b)
                #np[1] = (r,g,b)
                np.show()
                sleep(300)
                np.clear()
            except:
                continue