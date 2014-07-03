#!/usr/bin/env python

from nxt.brick import Brick
from nxt.locator import find_one_brick
from nxt.motor import Motor, PORT_A, PORT_B, PORT_C
from nxt.sensor import Light, Sound, Touch, Ultrasonic
from nxt.sensor import PORT_1, PORT_2, PORT_3, PORT_4
from nxt.bluesock import BlueSock

import os
import time
import signal
import sys
import json

MAC = '00:16:53:03:58:C6'

DEFAULT_POWER = 30

class Plotter:
    #idk how to make enums in python
    LOWERED, RAISED = 0, 1
    STOPPED, RUNNING = 0, 1

    def __init__(self, mac=MAC):
        self.brick = BlueSock(mac).connect()
        print "brick found"
        self.x_motor = Motor(self.brick, PORT_B)
        self.y_motor = Motor(self.brick, PORT_C)
        self.x_motor_state = Plotter.STOPPED
        self.y_motor_state = Plotter.STOPPED
        self.x, self.y = 0, 0
        self.pen = Motor(self.brick, PORT_A)
        self.pen_state = Plotter.RAISED
        self.ultrasonic = Ultrasonic(self.brick, PORT_1)
        self.touch = Touch(self.brick, PORT_2)

    def lower_pen(self):
        if self.pen_state == Plotter.LOWERED: return
        self.pen.turn(30, 150, brake=True)
        self.pen_state = Plotter.LOWERED

    def raise_pen(self):
        if self.pen_state == Plotter.RAISED: return
        self.pen.turn(-30, 70, brake=False)
        self.pen_state = Plotter.RAISED
        
    def toggle_pen(self):
        if self.pen_state == Plotter.LOWERED: self.raise_pen()
        else: self.lower_pen()

    def start_x(self, power=DEFAULT_POWER):
        if self.x_motor_state == Plotter.RUNNING: return
        self.x_motor.run(power=power, regulated=True)
        self.x_motor_state = Plotter.RUNNING

    def stop_x(self):
        self.x_motor.idle()
        self.x_motor_state = Plotter.STOPPED
    
    def start_y(self, power=DEFAULT_POWER):
        if self.y_motor_state == Plotter.RUNNING: return
        self.y_motor.run(power=-power, regulated=True)# * 0.9275)
        self.y_motor_state = Plotter.RUNNING

    def stop_y(self):
        self.y_motor.brake()
        self.y_motor_state = Plotter.STOPPED

    def turn_off(self):
        self.x_motor.idle()
        self.y_motor.idle()
        if self.pen_state == Plotter.LOWERED: self.raise_pen()

