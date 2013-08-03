__author__ = 'elemental'

from actor import *
import math

DEBUG = True


def mph_to_fps(miles_p_h):
    return miles_p_h * 1.4666


class Car(Actor):

    def __init__(self, path, w, turn='right'):
        self.velocity = 30
        self.path = path
        self.path_cell_id = self.path.enter_index
        Actor.__init__(self, self.path.enter, w)

        self.pos_x = self.cell.x * self.cell.total_length
        self.pos_y = self.cell.y * self.cell.total_length

        self.direction = 0
        self.facing = self.path.c_facing[self.path_cell_id]
        self.at_intersection = False
        self.turn = turn
        self.dist_x = 0
        self.dist_y = 0
        self.distance_till_cell = self.cell.total_length

    def set_path(self, p):
        self.path = p

    def check_and_set_next_cell_collision(self, c):
        temp_c, temp_path_cell_id, temp_p = c
        if temp_c.occupied:
            self.cell, self.path_cell_id, self.path = c
            return True
        else:
            return False

    def move_forward(self, delta):
        self.cell.occupied = False
        delta /= 1000.0
        temp_t = mph_to_fps(self.velocity)

        self.dist_x = math.cos(self.facing) * temp_t * delta
        self.dist_y = math.sin(self.facing) * temp_t * delta

        self.pos_x += self.dist_x
        self.pos_y += self.dist_y

        if self.distance_till_cell <= 0:
            remaing_dist = math.fabs(self.distance_till_cell)
            if self.path.at_intersection(self.cell):
                self.change_cell(self.turn, remaing_dist)
            else:
                self.change_cell(r_dist=remaing_dist)
        else:
            self.distance_till_cell -= math.fabs(self.dist_x) + math.fabs(self.dist_y)

        #if self.path.at_intersection(self.cell):
            #self.path = self.path.lead_into_path[self.turn]
            #updating the cell and path_cell_id is important, but atm this causes moving at intersections
            #because of a few things most importantly the fact that the paths that intersections contain
            #dont overlap with paths outside of intersection
        #    self.change_cell(self.turn)
            #temp_c, temp_path_cell_id, temp_p = self.path.next_cell(self.direction, self.path_cell_id, self.turn)
            #if not temp_c.occupied:
            #    self.cell, self.path_cell_id, self.path = temp_c, temp_path_cell_id, temp_p
            #    self.cell.distance = 0
        #else:
        #    self.change_cell()
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

    def change_cell(self, turn='c', r_dist=0):
        temp_c, temp_path_cell_id, temp_p = self.path.next_cell(self.direction, self.path_cell_id, turn)
        if not temp_c.occupied:
            self.cell, self.path_cell_id, self.path = temp_c, temp_path_cell_id, temp_p
            self.facing = self.path.c_facing[self.path_cell_id]
            self.distance_till_cell = self.cell.total_length - r_dist

    def turn_right(self):
        if self.path.at_intersection(self.cell):
            self.path = self.path.lead_into_path['right']

    def turn_left(self):
        if self.path.at_intersection(self.cell):
            self.path = self.path.lead_into_path['left']

    def go_straight(self):
        if self.path.at_intersection(self.cell):
            self.path = self.path.lead_into_path['straight']

    def at_stoplight(self):
        if self.cell.contains_stoplight:
            if self.distance_till_cell < 10: # or waiting behind car
                return True
            else:
                return False
        else:
            return False

    def slow_down_approach(self):
        pass

    def act(self, delta):
        if self.at_stoplight():
            s = self.cell.stoplight
            if s == 'green':
                self.move_forward(delta)
        else:
            self.move_forward(delta)
        #
        #if self.id == 17:
        #    pass
        #s = 'green'
        #if self.cell.contains_stoplight:
        #    s = self.cell.stoplight
        #if s == 'green':
        #    self.move_forward(delta)