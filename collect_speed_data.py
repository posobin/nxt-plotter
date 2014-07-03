#!/usr/bin/env python

import json
import sys
import time

from plotter import Plotter

CALIBRATION_DISTANCE = 50
MINIMUM_DISTANCE = 5

def main():
    p = Plotter()

    speeds = {}
    for power in range(30, 80):
        print "testing power =", power
        start_distance = p.ultrasonic.get_sample()
        print "start distance:", start_distance
        start = time.time()

        p.start_x(power=power)
        while (not p.touch.get_sample()): continue
        stop = time.time()
        p.stop_x()

        distance = CALIBRATION_DISTANCE #- (start_distance - MINIMUM_DISTANCE)
        print "total distance:", distance
        print "time:", stop - start
        speed = distance / (stop - start)
        print "speed:", speed
        speeds[power] = speed

        p.start_x(power=-40)
        while (p.ultrasonic.get_sample() > 13): continue
        p.start_x(power=-10)
        while (p.ultrasonic.get_sample() > 6): continue
        p.stop_x()
        print

    print "saving collected data"
    with open('speed_data/speed_x_data', 'w') as f: json.dump(speeds, f)
    print "data saved"

    p.turn_off()

if __name__ == "__main__":
    main()
