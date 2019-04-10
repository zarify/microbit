from microbit import *
import radio

radio.config(channel=50)

active = False
display.show(Image.NO)


while True:
    # use accelerometer for forward/back/left/right
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    a = button_a.was_pressed()
    b = button_b.was_pressed()

    if a and b:
        active = not active
        if active:
            display.show(Image("99900:00090:99009:00909:90909"))
            radio.on()
        else:
            display.show(Image.NO)
            radio.off()

    if not active:
        sleep(100)
        continue

    # left/right
    if x < -500: # left
        radio.send("left")
    elif x > 500:
        radio.send("right")
    # back/forward
    if y < -500:
        radio.send("forward")
    elif y > 500:
        radio.send("back")
    # flashy lights
    if a:
        radio.send("flash 100 0 0")
    elif b:
        radio.send("flash 0 0 100")

    sleep(700)