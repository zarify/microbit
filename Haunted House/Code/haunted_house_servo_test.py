from microbit import i2c
# the following imports are for the example code at the end of the file
from microbit import sleep
from random import randint, choice
import radio

class KitronikServoBoard:
    #
    # This class is used to drive the Kitronik 16 Servo add on for microbit
    # www.kitronik.co.uk/5612

    # Some useful parameters

    # In the future there may be several 16 Servo boards
    # all controlled from a single micro:bit
    # In that case extend the functions to include more board addresses
    # or pass an address in a constructor for the object to know.
    BOARD_1 = 0x6A

    # the prescale register address
    PRESCALE_REG = 0xFE

    # The mode 1 register address
    MODE_1_REG = 0x00

    # If you wanted to write some code that stepped through
    # the servos then this is the Base and size to do that
    SERVO_1_REG_BASE = 0x08
    SERVO_REG_DISTANCE = 4

    # To get the PWM pulses to the correct size and zero
    # offset these are the default numbers.
    SERVO_MULTIPLIER = 226
    SERVO_ZERO_OFFSET = 0x66

    # a flag to allow us to initialise without explicitly
    # calling the secret incantation
    INITALISED = False

    class Servos:
        # nice big list of servos to use.
        # These represent register offsets in the PCA9865
        SERVO_1 = 0x08
        SERVO_2 = 0x0C
        SERVO_3 = 0x10
        SERVO_4 = 0x14
        SERVO_5 = 0x18
        SERVO_6 = 0x1C
        SERVO_7 = 0x20
        SERVO_8 = 0x24
        SERVO_9 = 0x28
        SERVO_10 = 0x2C
        SERVO_11 = 0x30
        SERVO_12 = 0x34
        SERVO_13 = 0x38
        SERVO_14 = 0x3C
        SERVO_15 = 0x40
        SERVO_16 = 0x44

    # Trim the servo pulses. These are here for advanced users,
    # It appears that servos I've tested are actually expecting
    # 0.5 - 2.5mS pulses, not the widely reported 1-2mS.
    # that equates to multiplier of 226, and offset of 0x66
    # a better trim function that does the maths for the end
    # user could be written, the basics are here for reference

    def trim_servo_multiplier(self, trim_value):
        if trim_value < 113:
            self.SERVO_MULTIPLIER = 113

        else:
            if trim_value > 226:
                self.SERVO_MULTIPLIER = 226
            else:
                self.SERVO_MULTIPLIER = trim_value

    def trim_servo_zero_offset(self, trim_value):
        if trim_value < 0x66:
            self.SERVO_ZERO_OFFSET = 0x66
        else:
            if (trim_value > 0xCC):
                self.SERVO_ZERO_OFFSET = 0xCC
            else:
                self.SERVO_ZERO_OFFSET = trim_value

    def _secret_incantation(self):
        # This secret incantation sets up the PCA9865 I2C driver chip to
        # be running at 50Hz pulse repetition, and then sets the 16 output
        # registers to 1.5mS - centre travel on the servos.
        # It should not need to be called directly be a user -
        # the first servo write will call it.

        buf = bytearray(2)
        # Should really do a soft reset of the I2C chip here
        # First set the prescaler to 50 hz
        buf[0] = self.PRESCALE_REG
        buf[1] = 0x85
        i2c.write(self.BOARD_1, buf, False)
        # Block write via the all leds register to set all of them to 90 deg
        buf[0] = 0xFA
        buf[1] = 0x00
        i2c.write(self.BOARD_1, buf, False)
        buf[0] = 0xFB
        buf[1] = 0x00
        i2c.write(self.BOARD_1, buf, False)
        buf[0] = 0xFC
        buf[1] = 0x66
        i2c.write(self.BOARD_1, buf, False)
        buf[0] = 0xFD
        buf[1] = 0x00
        i2c.write(self.BOARD_1, buf, False)
        # Set the mode 1 register to come out of sleep
        buf[0] = self.MODE_1_REG
        buf[1] = 0x01
        i2c.write(self.BOARD_1, buf, False)
        # set the initalised flag so we dont come in here again automatically
        self.INITALISED = True

    def servo_write(self, Servo: Servos, degrees):
        # sets the requested servo to the reguested angle.
        # if the PCA has not yet been setup calls the initialisation routine
        # @param Servo Which servo to set
        # @param degrees the angle to set the servo to
        if self.INITALISED is False:
            self._secret_incantation(self)
        buf = bytearray(2)
        HighByte = False
        deg100 = degrees * 100
        PWMVal100 = deg100 * self.SERVO_MULTIPLIER
        PWMVal = PWMVal100 / 10000
        PWMVal = PWMVal + self.SERVO_ZERO_OFFSET
        if (PWMVal > 0xFF):
            HighByte = True
        buf[0] = Servo
        buf[1] = int(PWMVal)
        i2c.write(self.BOARD_1, buf, False)
        if (HighByte):
            buf[0] = Servo + 1
            buf[1] = 0x01
        else:
            buf[0] = Servo + 1
            buf[1] = 0x00
        i2c.write(self.BOARD_1, buf, False)

#--------------------------------------------------------------
# Board config
theServoBoard = KitronikServoBoard
radio.config(channel=42)
radio.on()

class Window():
    def __init__(self, up=41, down=135, servo=None, name="", short_name="", controller=None):
        self.up = up
        self.down = down
        self.servo = servo
        self.name = name
        self.short_name = short_name
        self.controller = controller
        self.current = down
        self.in_queue = False
    
    def move(self, reset=False):
        "Toggle the position of this servo, or move it down if reset is True."
        if reset:
            self.controller.servo_write(self.controller, self.servo, self.down)
            self.current = self.down
            self.in_queue = False
        else:
            angle = self.up if self.current == self.down else self.down
            self.controller.servo_write(self.controller, self.servo, angle)
            self.current = angle
            if self.is_up(): # de-queue if this servo has moved up
                self.in_queue = False
    
    def queue(self, uptime, downtime):
        "Queue up this servo to move up and down at the specified running times."
        self.uptime = uptime
        self.downtime = downtime
        self.in_queue = True
        
    def is_up(self):
        "Compare current angle with 'up' state and return True if equal."
        return True if self.current == self.up else False
    
    def in_queue(self):
        "Return true if this servo is in the queue and not currently up."
        return True if self.in_queue and not self.is_up() else False
    
    def check_queue(self, now):
        """
        Pass in the current running time. Check whether this requires the servo
        to change position, and return an appropriate message.
        """
        if self.in_queue():
            if now > self.uptime:
                self.move()
                return "moved up"
            elif now > self.downtime:
                self.move()
                return "moved down"
        return "no change"
    
    def __repr__(self):
        return "Servo {}\n\tCurrent angle: {}\n\tIn queue: {}\n\tIs up: {}".format(self.name, self.current, self.in_queue(), self.is_up())

#--------------------------------------------------------------
# Game config

# House windows, seen from front of house
#
# tl    tm      tr
#
# bl            br
windows = {
    "tl": Window(up=41, down=135, servo=KitronikServoBoard.Servos.SERVO_1,
        name="Top Left", short_name="tl", controller=theServoBoard),
    "tm": Window(up=41, down=135, servo=KitronikServoBoard.Servos.SERVO_1,
        name="Top Middle", short_name="tm", controller=theServoBoard),
    "tr": Window(up=41, down=135, servo=KitronikServoBoard.Servos.SERVO_1,
        name="Top Right", short_name="tr", controller=theServoBoard),
    "bl": Window(up=41, down=135, servo=KitronikServoBoard.Servos.SERVO_1,
        name="Bottom Left", short_name="bl", controller=theServoBoard),
    "br": Window(up=50, down=130, servo=KitronikServoBoard.Servos.SERVO_1,
        name="Bottom Right", short_name="br", controller=theServoBoard)
}
# score, running state, difficulty
game_state = {
    "score": 0, # integer
    "state": False, # off/on
    "difficulty": 1, # increments to reduce time enemies are up
    "servos_up": lambda: len([x for x in windows if x.is_up()]), # how many servos are currently up
    "servo_queue_len": lambda: len([x for x in windows if x.in_queue()]), # how many servos are in the queue
    "last_in_queue": lambda: sorted([x for x in windows if x.in_queue()], key=lambda x: x.downtime)[-1]
}

def next_servo():
    """
    Pick the next servo to be raised and the delay until it comes up.
    
    """
    global windows
    # pick a servo that is not already in the queue or up
    ns = choice([windows[s] for s in windows if not windows[s].in_queue()])
    
    # TODO: add in a difficulty modifier, just use whole seconds for testing
    delay = randint(1, 6) * 1000
    duration = randint(2, 5) * 1000
    
    # add this servo's data to the game state
    # set the start time of the next pop up to either the current running time (no servos up)
    # or start it from when the last servo in the queue comes up
    now = running_time() if game_state["servo_queue_len"]() == 0 else game_state["last_in_queue"]().uptime
    when_up = now + delay
    when_down = when_up + 1000 * duration
    ns.queue(when_up, when_down)
    print("\tQueued servo {} up: {} down {}".format(ns.short_name, when_up, when_down))

# reset all servos to 'down' state
for window in windows:
    window.move(reset=True)

game_state["score"] = 0
game_state["state"] = True

# broadcast a game reset message
radio.send("servo reset")
# add two servos to start with
next_servo()
next_servo()

while True:
    # Check on the servo queue for whether we need to raise or lower one
    now = running_time()
    for w in windows:
        r = w.check_queue(now)
        if r == "moved up":
            print("Servo {} moving UP".format(w.short_name))
            radio.send("servo up "+w.short_name)
        elif r == "moved down":
            print("Servo {} moving DOWN".format(w.short_name))
            radio.send("servo down "+w.short_name)
    while game_state["servo_queue_len"]() < 2:
        print("Queueing up a new servo:")
        next_servo()
    # check for received messages
    #   
    r = radio.receive()
    if r:
        if r.startswith("window hit "):
            print("Servo {} hit!".format(r[-2:]))
            if windows[r[-2:]].is_up():
                windows[r[-2:]].move()
            else:
                print("\tServo {} hit but not up!".format(r[-2:]))
    sleep(50)
