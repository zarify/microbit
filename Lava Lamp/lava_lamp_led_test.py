from microbit import *
import neopixel
from random import randint

np = neopixel.NeoPixel(pin12, 1)
h, s, v = (0.0, 1.0, 0.5) # initial colour values
targ = v # target value to shift to, will immediately calculate a new one
direction = 1 # will be overwritten as soon as a target value is found
step = 0.001 # speed of brightness and hue transitions

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

def get_new_trend(v):
  # Calculate a new target brightness value, and return the
  # new value and the direction multiplier for the step value.
  tl = randint(1, 4) / 10
  # choose direction for trend (-ve dimmer, +ve brighter)
  if (v + tl) >= 1.0:
    td = -1
  elif (v - tl) <= 0.1:
    td = 1
  else:
    td = -1 if randint(1,2) == 1 else 1
  to = round(v + tl * td, 1)

  return (to, td) # return the new target value and direction

while True:
  a = button_a.was_pressed()
  b = button_b.was_pressed()

  h = (h + step) % 1 # cycle through hue space
  if (direction == -1 and v >= targ) or (direction == 1 and v <= targ):
    v += step * direction
  else:
    targ, direction = get_new_trend(v)

  (r, g, b) = hsv_to_rgb(h, s, v)
  np[0] = (int(r), int(g), int(b))
  np.show()
  sleep(50)