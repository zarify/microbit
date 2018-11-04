from microbit import pin0, pin1, pin2, pin3, pin4, pin6, pin7, pin8, pin9, pin12, display, sleep
import radio

# This board needs to communicate with the servos so that when the LDR is triggered
# the servo board can be told to put down that monster. Also it means if a scoreboard
# microbit is added then it can listen to this for score totals.
radio.config(channel=42)
radio.on()

# Disable the display so that we can use the pins reserved for the display.
display.off()

class Window():
    """
    Haunted house window controls. Comprised of a light dependent resistor,
    a servo (controlled by a separate board slotted into a Kitronik 16 servo
    controller board) and a transistor, which is used like a relay to toggle
    external power (6V battery) to pairs of LEDs.
    """
    def __init__(self, ldr_pin, led_pin, name, short_name):
        self.led = led_pin
        self.ldr = ldr_pin
        self.name = name
        self.led_state = False
        self.led.write_digital(1) # power the transistor on startup to turn off LEDs
        self.short_name = short_name

    def light(self):
        return self.ldr.read_analog()
    
    def hit_test(self):
        "Return True if a bright light is detected, but only if the LEDs are on (servo is in up state)."
        return self.light() > 900 if self.led_state else False
    
    def short(self):
        return self.short_name
    
    def toggle_led(self):
        if self.led_state:
            self.led.write_digital(1)
        else:
            self.led.write_digital(0)
        self.led_state = not self.led_state
    
    def __repr__(self):
        return "{}: PVR: {} LED: {} []".format(self.name, self.ldr, self.led, "on" if self.led_state else "off")

# Initialise the different windows
# Pins 0-4 are available for analog reads, 5 and 11 are reserved
# for buttons and can't be disabled as such (unlike the display)
# 6 - 9 and 12 can be used for digital writes.
tl = Window(pin0, pin12, "Top Left", "tl")
bl = Window(pin1, pin6, "Bottom Left", "bl")
tr = Window(pin2, pin7, "Top Right", "tr")
br = Window(pin3, pin8, "Bottom Right", "br")
tm = Window(pin4, pin9, "Top Middle", "tm")

# Mapping for message queue lookups
windows = { "tl": tl, "bl": bl, "tr": tr, "br": br, "tm": tm }

while True:
    # Cycle through windows and see if any active windows have been zapped
    for w in (tl, tr, bl, br, tm):
        if w.hit_test():
            # notify the servo board which window has been hit and turn off the LEDs
            radio.send("window hit "+w.short())
            w.toggle_led()
    # Parse message queue
    r = radio.receive()
    if r:
        # servo board has communicated that a servo has been moved up or down
        # so toggle the LED state for this window
        if r.startswith("servo down ") or r.startswith("servo up "):
            windows[r[-2:]].toggle_led()
            
    
    sleep(50)