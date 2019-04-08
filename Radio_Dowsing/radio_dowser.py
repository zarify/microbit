from microbit import *
import radio

radio.config(channel=42,power=2)
radio.on()

while True:
    # radio.send("ping") # uncomment for both send and receive behaviour
    r = radio.receive_full()
    if r:
        msg, rssi, ts = r
        print((rssi,))
        if rssi > -60:
            display.show(Image("99999:00000:00000:00000:00000"))
        elif rssi > -70:
            display.show(Image("00000:99999:00000:00000:00000"))
        elif rssi > -80:
            display.show(Image("00000:00000:99999:00000:00000"))
        elif rssi > -90:
            display.show(Image("00000:00000:00000:99999:00000"))
        elif rssi > -100:
            display.show(Image("00000:00000:00000:00000:99999"))
        else:
            display.clear()
    else:
        display.clear()
    sleep(50)