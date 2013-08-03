__author__ = 'elemental'

from actor import *


class TrafficLight(Actor):
    def __init__(self, cell=None, world=None):
        Actor.__init__(self, cell, world)
        self.current_sid = 0
        self.states = ['green', 'yellow', 'red']
        self.state_times = [10, 3, 6]
        self.time_pasted = 0
        self.current_state = self.set_state()

    def set_cell(self, c):
        Actor.set_cell(self, c)
        self.cell.contains_stoplight = True

    def set_state(self):
        self.current_state = self.states[self.current_sid % len(self.states)]

    def act(self, delta):

        self.time_pasted += (delta/1000.0)

        if self.time_pasted >= self.state_times[self.current_sid % 3]:
            self.current_sid += 1
            self.time_pasted = 0

        self.set_state()
        self.cell.stoplight = self.current_state