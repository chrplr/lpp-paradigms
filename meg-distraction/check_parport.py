#! /usr/bin/env python


import time
from expyriment import io
pp = io.ParallelPort('/dev/parport1')
print('The LEDs on the STI box should blink every sec')

while True:
    pp.set_data(0)
    time.sleep(1)
    pp.set_data(255)
    time.sleep(1)
