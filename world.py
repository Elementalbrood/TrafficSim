__author__ = 'elemental'

from path import *
from actor import Actor
from car import Car


class World:
    EMPTY = 0
    PATH = 1
    INTERSECTION = 2
    CAR = 3
    TRAFFICLIGHT_RED = 4
    TRAFFICLIGHT_YELLOW = 5
    TRAFFICLIGHT_GREEN = 6

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[World.EMPTY for _ in range(width)] for _ in range(height)]
        self.terrian = [[World.EMPTY for _ in range(width)] for _ in range(height)]
        self.sents = [[World.EMPTY for _ in range(width)] for _ in range(height)]
        self.actors = {}
        self.paths = {}
        self.clear_canvas()
        self.print_interval = 0

    def add_actor(self, a):
        if isinstance(a, Actor):
            try:
                if self.actors[a.id] == a:
                    if DEBUG:
                        print('Actor as already been added to the world')
            except KeyError:
                pass

            if a.cell is not None:
                self.actors[a.id] = a
            else:
                if DEBUG:

                    print('Actor does not have a cell')
        elif DEBUG:
            print('tried to add something that is not an actor')

    def add_paths(self, path_l):
        for i in path_l:
            self.add_path(i)

    def add_path(self, p):
        self.paths[p.id] = p
        self.update_grid(p)

    def update_grid(self, c):
        if isinstance(c, Path):
            for i in c.m_path.values():
                self.terrian[i.y][i.x] = World.PATH
        elif isinstance(c, Two_by_Two):
            for i in range(2):
                for j in range(2):
                    self.terrian[j+c.coord.y][i+c.coord.x] = World.INTERSECTION

    def add_intersections(self, inter_list):
        for i in inter_list:
            self.add_intersection(i)

    def add_intersection(self, i):
        if isinstance(i, Two_by_Two):
            for j in i.traffic_lights.values():
                if j.cell is not None:
                    self.add_actor(j)
            self.add_2_2_inter(i)

    def add_2_2_inter(self, i):
        self.update_grid(i)

    def start(self):
        for i in self.actors.values():
            i.start()

    def __getitem__(self, j):
        return self.grid[j]

    def clear_canvas(self):
        self.canvas = [[World.EMPTY for _ in range(self.width)] for _ in range(self.height)]

    def draw_terrain(self):
        for i in range(self.height):
            for j in range(self.width):
                self.canvas[i][j] = self.terrian[i][j]

    def draw_actors(self):
        for i in self.actors.values():
            if isinstance(i, Car):
                self.canvas[i.cell.y][i.cell.x] = World.CAR
            elif isinstance(i, TrafficLight):
                if i.current_state == 'red':
                    self.canvas[i.cell.y][i.cell.x] = World.TRAFFICLIGHT_RED
                elif i.current_state == 'yellow':
                    self.canvas[i.cell.y][i.cell.x] = World.TRAFFICLIGHT_YELLOW
                elif i.current_state == 'green':
                    self.canvas[i.cell.y][i.cell.x] = World.TRAFFICLIGHT_GREEN

    def update_canvas(self):
        self.draw_terrain()
        self.draw_actors()

    def print_world(self):

        self.update_canvas()

        for i in self.canvas:
            for j in i:
                print(str(j) + "\n")
            print("")

    def add_roads(self, road_list):
        for i in road_list:
            for p in i.paths.values():
                self.add_path(p)

    #delta will be in milliseconds
    def update(self, delta):

        for i in self.actors.values():
            i.act(delta)

        self.update_canvas()