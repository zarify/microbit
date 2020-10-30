from microbit import i2c
from microbit import sleep, running_time
from random import randint, choice

class KitronikServoBoard:
    BOARD_1 = 0x6A
    PRESCALE_REG = 0xFE
    MODE_1_REG = 0x00
    SERVO_1_REG_BASE = 0x08
    SERVO_REG_DISTANCE = 4
    SERVO_MULTIPLIER = 226
    SERVO_ZERO_OFFSET = 0x66
    INITALISED = False

    class Servos:
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
        buf = bytearray(2)
        buf[0] = self.PRESCALE_REG
        buf[1] = 0x85
        i2c.write(self.BOARD_1, buf, False)
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
        buf[0] = self.MODE_1_REG
        buf[1] = 0x01
        i2c.write(self.BOARD_1, buf, False)
        self.INITALISED = True

    def servo_write(self, Servo: Servos, degrees):
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

class ServoController:
    board = KitronikServoBoard
    # Servo, UpAngle, DownAngle, IsUp, InQueue, CurrentAngle, UpTime, DownTime
    #    0      1         2        3      4         5           6         7
    servos = {
        "tl": [KitronikServoBoard.Servos.SERVO_1, 41, 135, False, False, 0, 0, 0],
        "tm": [KitronikServoBoard.Servos.SERVO_8, 41, 135, False, False, 0, 0, 0],
        "tr": [KitronikServoBoard.Servos.SERVO_15, 41, 135, False, False, 0, 0, 0],
        "bl": [KitronikServoBoard.Servos.SERVO_2, 41, 135, False, False, 0, 0, 0],
        "br": [KitronikServoBoard.Servos.SERVO_16, 50, 127, False, False, 0, 0, 0]
    }
 
    def move(self, servo, reset=False):
        if reset:
            self.board.servo_write(self.board, self.servos[servo][0], self.servos[servo][2]) # move down
            self.servos[servo][3] = False # not up
            self.servos[servo][4] = False # not in queue
            self.servos[servo][5] = self.servos[servo][2] # current angle to down
        else:
            angle = self.servos[servo][1] if self.servos[servo][5] == self.servos[servo][2] else self.servos[servo][2]
            self.board.servo_write(self.board, self.servos[servo][0], angle)
            self.servos[servo][5] = angle
    
    def check_queue(self, now):
        for servo in self.servos:
            if self.servos[servo][4] and now > self.servos[servo][6]:
                self.servos[servo][4] = False
                self.servos[servo][3] = True
                self.move(self, servo, reset=False)
            elif self.servos[servo][3] and now > self.servos[servo][7]:
                self.move(self, servo, reset=False)
                self.servos[servo][3] = False
                self.next_servo(self)
    
    def next_servo(self):
        try:
            max_up = max([self.servos[s][6] for s in self.servos if self.servos[s][4]])
        except ValueError:
            max_up = 0
        now = running_time() if max_up == 0 else max_up
        
        ns = choice([s for s in self.servos if not self.servos[s][4] and not self.servos[s][3] and now ])
        
        when_up = now + randint(1, 6) * 1000
        when_down = when_up + 1000 * randint(2, 5)
        self.servos[ns][4] = True
        self.servos[ns][6] = when_up
        self.servos[ns][7] = when_down

SC = ServoController

score = 0
difficulty = 1

for s in ("tl", "tm", "tr", "bl", "br"):
    SC.move(SC, s, reset=True)

SC.next_servo(SC)
SC.next_servo(SC)

while True:
    now = running_time()
    SC.check_queue(SC, now)

    sleep(50)