__author__ = 'elemental'

from actor import *
import math

DEBUG = True


class Car(Actor):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, path, w, turn='right'):
        self.pos_x = 0
        self.pos_y = 0
        self.velocity = 40
        self.direction = Car.NORTH
        self.path = path
        self.path_cell_id = self.path.enter_index

        Actor.__init__(self, self.path.enter, w)
        self.direction = 0
        self.at_intersection = False
        self.turn = turn

    def set_path(self, p):
        self.path = p

    def check_and_set_next_cell_collision(self, c):
        temp_c, temp_path_cell_id, temp_p = c
        if temp_c.occupied:
            self.cell, self.path_cell_id, self.path = c
            return True
        else:
            return False

    def move_forward(self):
        self.cell.occupied = False
        if self.path.at_intersection(self.cell):
            #self.path = self.path.lead_into_path[self.turn]
            #updating the cell and path_cell_id is important, but atm this causes moving at intersections
            #because of a few things most importantly the fact that the paths that intersections contain
            #dont overlap with paths outside of intersection
            self.change_cell(self.turn)
            #temp_c, temp_path_cell_id, temp_p = self.path.next_cell(self.direction, self.path_cell_id, self.turn)
            #if not temp_c.occupied:
            #    self.cell, self.path_cell_id, self.path = temp_c, temp_path_cell_id, temp_p
            #    self.cell.distance = 0
        else:
            self.change_cell()
            #temp_c, temp_path_cell_id, temp_p = self.path.next_cell(self.direction, self.path_cell_id)
            #if not temp_c.occupied:
            #    self.cell, self.path_cell_id, self.path = temp_c, temp_path_cell_id, temp_p
            #    self.cell.distance = 0
            #else:
            #    if DEBUG:
                    #print("Car is in front of me can't move")
            #        pass
            #self.cell, self.path_cell_id, self.path = self.path.next_cell(self.direction, self.path_cell_id)
        self.cell.occupied = True

    def change_cell(self, turn='c'):
        temp_c, temp_path_cell_id, temp_p = self.path.next_cell(self.direction, self.path_cell_id, turn)
        if not temp_c.occupied:
            self.cell, self.path_cell_id, self.path = temp_c, temp_path_cell_id, temp_p

    def turn_right(self):
        if self.path.at_intersection(self.cell):
            self.path = self.path.lead_into_path['right']

    def turn_left(self):
        if self.path.at_intersection(self.cell):
            self.path = self.path.lead_into_path['left']

    def go_straight(self):
        if self.path.at_intersection(self.cell):
            self.path = self.path.lead_into_path['straight']

    def act(self, delta):
        s = 'green'
        if self.cell.contains_stoplight:
            s = self.cell.stoplight
        if s == 'green':
            self.move_forward()