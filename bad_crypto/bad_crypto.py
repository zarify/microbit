from microbit import *
from random import randint
import radio

images = [Image.HEART, Image.HEART_SMALL, Image.HAPPY, Image.SMILE, Image.SAD, Image.CONFUSED,
    Image.ANGRY, Image.ASLEEP, Image.SURPRISED, Image.SILLY, Image.FABULOUS, Image.MEH, Image.YES,
    Image.NO, Image.TRIANGLE, Image.CHESSBOARD, Image.DIAMOND, Image.SQUARE, Image.XMAS, Image.TARGET,
    Image.HOUSE, Image.TORTOISE, Image.GHOST, Image.SWORD, Image.SKULL, Image.UMBRELLA, Image.SNAKE]

# Bitmasks to XOR our images with
# One mask for each channel, so each gets a different encrypted version of the same image
# encrypted view of the same image when listening on a different channel
#        _________________________
MASKS = [0b0100011011101100101001100, 0b0001100100001001110011000, 0b1001001011001110101100001, 0b0111110001111111001011100]
# First channel by default
CHANNEL = 1
# Default to sending and receiving in the clear
ENCRYPTING = 0

radio.on()
radio.config(channel=CHANNEL)

# Show the current channel for a second, then blank the screen
display.show(str(CHANNEL))
sleep(1000)
display.clear()

def str_image():
    """Look at the current display and build a bit string.
       Since each LED is stored as an intensity 0-9, convert
       to 1s and 0s instead so we can XOR them later."""
    out = ""
    for y in range(5):
        for x in range(5):
            if display.get_pixel(x,y) != 0:
                out += "1"
            else:
                out += "0"
    return out

def str_xor(s):
    """Take a string input, convert it to binary, and then XOR
       it with the MASK to encrypt or decrypt a string of bits.
       Pad out the length of the encoded string with 0s to cope
       with higher order bits of 0 being ignored.
       Return another string suitable for display or transmission.
    """
    global CHANNEL
    # Turn the bit string into a number
    n = int(s,2)
    enc = bin(n ^ MASKS[CHANNEL-1])[2:]
    while len(enc) < 25:
        enc = "0"+enc
    return enc

def display_string(s):
    """Take a decoded string of bits and display it on the LED
       screen.
    """
    display.clear()
    # maybe put a small delay in here to simulate the transmission?
    sleep(50)
    c_pos = 0
    for y in range(5):
        for x in range(5):
            if s[c_pos] == "1":
                display.set_pixel(x,y,9)
            else:
                display.set_pixel(x,y,0)
            c_pos += 1
            sleep(50)

def change_channel():
    """Cycle through 4 channels (can go up to 100!)
       First cycle will change to channel in clear text.
       Second cycle will be the same channel in encrypted mode.
       This way I can use the same program to demonstrate snooping
       and encrypting at once.
    """
    global CHANNEL
    global ENCRYPTING
    
    if ENCRYPTING:
        if CHANNEL == 4:
            CHANNEL = 1
        else:
            CHANNEL += 1
        ENCRYPTING = 0
    else:
        ENCRYPTING = 1
    radio.config(channel=CHANNEL)
    # show the channel on the screen for a second
    display.show(str(CHANNEL))
    # show an indicator in the top-right corner if we're encrypting
    if ENCRYPTING:
        display.set_pixel(4,0,9)
    sleep(1000)
    display.clear()

def pick_picture():
    p = randint(0,len(images)-1)
    display.show(images[p])

# Main loop
while True:
    # Shake - choose new picture
    # A - transmit picture
    # B - switch channel, also switch between clear and encrypt modes
    #     First press will 
    # Sleep after each action, rather than a general sleep at the end, since
    # we don't want to get locked in the loop snoozing while radio transmissions
    # are arriving.
    if accelerometer.was_gesture("shake"):
        pick_picture()
        sleep(30)
    if button_a.was_pressed():
        # get a bitstring of the screen
        s = str_image()
        # encrypt the string - could do s = str_xor(str_image()) in one step
        se = str_xor(s)
        if ENCRYPTING:
            radio.send(se)
        else:
            radio.send(s)
        sleep(30)
    elif button_b.was_pressed():
        change_channel()
        sleep(30)
    # receive code
    data = radio.receive()
    if data != None:
        if ENCRYPTING:
            s = str_xor(data)
            display_string(s)
        else:
            display_string(data)
        sleep(30)
    