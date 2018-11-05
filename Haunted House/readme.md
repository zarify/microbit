# Haunted House
This is a robotics project I was working on for myself in 2018 whilst teaching robotics as a Year 8 subject.
It was initially conceived as a simple servo-driven light gun game where enemies containing a photoresistor (LDR)
would pop up and down at random intervals and you zap them with a (non-computerised) LED gun.

The idea has grown into more of a Halloween theme, with glowing LED eyes for the enemies, and I have plans
to incorporate ammo and reloading into the gun design, which at the moment is stalled due to not finding a
satisfactory way to narrow the LED beam sufficiently. At this point I'm testing with a simple LED flashlight
that contains a focusing lens that gives an acceptable beam.

## Code
Code is in Micropython and currently split over two Microbit boards:
- [A Kitronik I2C 16 servo controller](https://www.kitronik.co.uk/5612-kitronik-i2c-servo-driver-board-for-the-bbc-microbit.html) using [their servo code](https://github.com/KitronikLtd/micropython-microbit-kitronik-16-servo-board) (MIT License)
- A standard Microbit for the LED and LDRs (I'm using a [Kitronik edge connector breakout board](https://www.kitronik.co.uk/5601b-edge-connector-breakout-board-for-bbc-microbit-pre-built.html) but anything will do there)
The two boards communicate via the Microbit's radio module for state syncing.

The LED/LDR board handles the LED state, which is controlled via a transistor, and contains
helper functions for toggling state, determining whether a light beam has hit the enemy and so on. The
servo board handles basic servo movement as well as keeping track of a queue for when to raise and lower
enemies.

I have tried to keep both bits of code as tight as possible timing-wise to help keep things in sync and not
block radio calls, but have included small event loop pauses for battery efficiency purposes and also to help
cope with events repeating too quickly for physical objects to keep up with.

## Design
The physical parts of the house were cut out of 3mm MDF on the school's laser cutter. My workflow for this is
needlessly complex, since I'm familiar with vector design and not CAD. Thus, all of my design has started out in
[Affinity Designer](https://affinity.serif.com/en-gb/designer/), which lacks a direct method of exporting to DXF
format for the laser cutter (but Adobe Illustrator does). This means my workflow turns into:
- Design in Affinity Designer
- Export to PSD (no AI export from Designer 😫)
- Import PSD into Illustrator
- Export to DXF

I have included my original Affinity files, the exported Illustrator files, and my final DXFs if anyone wants to
use them. (AI and DXF are coming.)

## Electronics
### Parts
The following parts are what I used for this project:
1. Cheap 9g servos (I paid about US$2 each for them)
2. 5mm Photoresistor
3. 100 Ohm, 1 kOhm, and 10 kOhm resistors (1 each per window)
4. 3mm LEDs (I used green - these turned out a bit too bright, I'd probably use a higher value resistor on them next time)
5. BC557B transistor

Total cost including the mini breadboards would be under $20. Since I wasn't really sure that my
circuits were going to work the way I expected them to, the only parts I soldered and hot glued
were the enemy assemblies. If I make a similar project in the future I'll get rid of the
breadboards and just solder the window assemblies and hot glue them to the back of the main MDF
board.

The real expense here is the Microbits (about $20 each) and the breakout boards (about $30). My aim is
to replace these with my own circuit for the servos and replacing the Microbits with ESP32
boards. That should bring the cost of the controllers down to about $12.