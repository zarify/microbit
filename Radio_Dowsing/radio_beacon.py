from microbit import *
import radio

strength = 2 # default strength for shortish range beacons
radio.config(channel=42,power=strength)
transmitting = False
display.show(Image.NO)

while True:
    # toggle radio activity with the A button
    if button_a.was_pressed():
        transmitting = not transmitting
        if not transmitting:
            display.show(Image.NO)
            radio.off()
        else:
            display.show(Image.YES)
            radio.on()
    elif button_b.was_pressed():
        # change the signal strength with B, between 0 and 3
        strength += 1
        if strength >= 4:
            strength = 0
        display.show(strength)
        radio.config(channel=42, power=strength)
        sleep(500)
        if transmitting:
            display.show(Image.YES)
        else:
            display.show(Image.NO)

    if transmitting:
        # can be anything, but "ping" is cute.
        radio.send("ping")

    sleep(50)