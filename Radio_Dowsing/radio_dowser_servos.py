from microbit import *
import radio
import neopixel

radio.config(channel=42)
display.show(Image.NO)
detecting = False

# rolling average of last X readings (1.5s)
last = []
keep_last = 25 # how long the rolling average should be
perc_avg = 0.0

np = neopixel.NeoPixel(pin0, 1) # just the one LED for now

def hsv_to_rgb(h, s, v):
    # Algorithm from: https://stackoverflow.com/a/26856771
    # Expects floats for all 3 arguments, so hue space is 0-1.
    if s == 0.0:
        v*=255
        return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i
    p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f))))
    v*=255
    i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def move_servos(a):
    right = (pin8, 40) # pin connected and base angle
    left = (pin12, 120)
    left[0].write_analog(left[1] + a)
    right[0].write_analog(right[1] - a)

def set_LEDs(p):
    r, g, b = hsv_to_rgb(1.0 - p, 1.0, 0.2) # take the percentage strength and map to hue
    np[0] = (int(r), int(g), int(b))
    np.show()

while True:
    if button_a.was_pressed():
        detecting = not detecting
        if detecting:
            display.show(Image("99900:00090:99009:00909:90909"))
            radio.on()
        else:
            display.show(Image.NO)
            radio.off()

    if not detecting:
        continue

    r = radio.receive_full()
    if r:
        msg, rssi, ts = r
        # nomalise the -255 to 0 strength to a 90 degree arc
        # but compress the range here, since realistically it seems to vary
        # from about -100 to -30
        rssi = abs(rssi) - 30
        if rssi < 0:
            rssi = 0
        elif rssi > 70:
            rssi = 70
        perc = rssi / 70

    else:
        perc = 1.0

    # Do this as a rolling average to smooth out spiky changes in signal strength
    last.append(perc)
    if len(last) > keep_last:
        del last[0]
    perc_avg = sum(last) / len(last)

    angle = 90 - int(perc_avg * 90) # subtract from 90 since 0 is strong, 255 weak

    #print((rssi, perc_avg, angle))

    # shift servos to this angle (accounting for two opposite sides)
    move_servos(angle)
    # change LED colours if relevant
    set_LEDs(perc_avg)
    # let servos move to any new positions before checking again
    sleep(50)