from microbit import *

prev = pin1.read_digital() # pin 1

counter = 0
rt = running_time()

while True:
    p1 = pin1.read_analog() # dt
    p2 = pin2.read_analog() # cw
    p1 = 0 if p1 < 500 else 1
    p2 = 0 if p2 < 500 else 1

    a = (pin0.read_analog() < 200) and (running_time() - rt) > 1000
    if a:
        print("Counter:",counter)
        rt = running_time()

    if p2 != prev:
        if p1 != prev:
            counter -= 1
        else:
            counter += 1

        prev = 0 if pin2.read_analog() < 500 else 1

