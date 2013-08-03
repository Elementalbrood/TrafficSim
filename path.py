__author__ = 'elemental'

DEBUG = True

import math
from collections import defaultdict
from trafficlight import TrafficLight


class Path:
    NORTH = math.pi/2.0
    EAST = 0.0
    SOUTH = (3*math.pi)/2.0
    WEST = math.pi
    next_id = 0
    EXIT_AWAY = 0
    ENTER_AWAY = 1

    def __init__(self, d=0, file_id=-1):
        self.enter = None
        self.enter_index = None
        self.exit = None
        self.exit_index = None
        self.enter_sign = -1
        self.exit_sign = 1
        self.m_path = {}
        self.c_facing = {}
        self.exit_inter_cell = 0
        self.enter_inter_cell = 0
        self.direction = d % 2
        self.dead_end = True
        if file_id != -1:
            self.id = file_id
        else:
            self.id = Path.next_id
            Path.next_id += 1
        self.cell_id = 0
        self.lead_into_path = defaultdict(int)

    def clear_path(self):
        self.enter = None
        self.enter_index = None
        self.exit = None
        self.exit_index = None
        self.enter_sign = -1
        self.exit_sign = 1
        self.m_path = {}
        self.c_facing = {}
        self.exit_inter_cell = 0
        self.enter_inter_cell = 0
        self.cell_id = 0
        self.lead_into_path = defaultdict(int)
        self.dead_end = True

    def set_path_from_to(self, x1, y1, x2, y2):
        """

        :param x1:
        :param y1:
        :param x2:
        :param y2:
        this will clear the current path and reset it with the given info
        """
        self.clear_path()
        if not (x1 == x2 or y1 == y2):
            print('error not horizontal or vertical')
            return False
        if x1 == x2:

            i = y1
            #c = sign(y1 - y2) * -1
            c = int((y1 - y2)/int(math.fabs(y1 - y2))) * -1
            while i != y2+c:
                self.add_cell(x1, i)
                i += c

        elif y1 == y2:
            i = x1
            #c = sign(x1 - x2) * -1
            c = int((x1 - x2)/int(math.fabs(x1 - x2))) * -1
            while i != x2+c:
                self.add_cell(i, y1)
                i += c

        return True

    def add_cell(self, x, y):
        if len(self.m_path) == 0:
            self.m_path[0] = Cell(x, y)
            self.enter = self.m_path[0]
            self.enter_index = 0
            self.exit = self.m_path[0]
            self.exit_index = 0
        else:
            c = Cell(x, y)
            if self.direction == Path.EXIT_AWAY:
                if not self.add_exit(c):
                    self.add_enter(c)
            elif self.direction == Path.ENTER_AWAY:
                if not self.add_enter(c):
                    self.add_exit(c)

    def add_Cell(self, c):
        if len(self.m_path) == 0:
            self.m_path[0] = c
            self.enter = self.m_path[0]
            self.enter_index = 0
            self.exit = self.m_path[0]
            self.exit_index = 0
        else:
            if self.direction == Path.EXIT_AWAY:
                if not self.add_exit(c):
                    self.add_enter(c)
            elif self.direction == Path.ENTER_AWAY:
                if not self.add_enter(c):
                    self.add_exit(c)

    def add_enter(self, cell):
        if man_hat(self.enter.x, self.enter.y, cell.x, cell.y) == 1:
            self.enter_index += self.enter_sign
            self.m_path[self.enter_index] = cell
            self.enter = cell

            c1 = self.m_path[self.enter_index - self.enter_sign]
            d = get_facing(self.enter, c1)
            if d != -1:
                self.c_facing[self.enter_index] = d

            return True
        return False

    def add_exit(self, cell):
        if man_hat(self.exit.x, self.exit.y, cell.x, cell.y) == 1:
            self.exit_index += self.exit_sign
            self.m_path[self.exit_index] = cell
            self.exit = cell

            c1 = self.m_path[self.exit_index - self.exit_sign]
            d = get_facing(c1, self.exit)
            if d != -1:
                self.c_facing[self.exit_index - self.exit_sign] = d
                self.c_facing[self.exit_index] = d
            return True
        return False

    def switch_direction(self):
        temp_c = self.enter
        self.enter = self.exit
        self.exit = temp_c
        temp_i = self.exit_index
        self.exit_index = self.enter_index
        self.enter_index = temp_i
        self.enter_sign *= -1
        self.exit_sign *= -1
        for i in self.c_facing.keys():
            self.c_facing[i] = flip_facing(self.c_facing[i])

        self.c_facing[self.enter_index] = get_facing(self.enter, self.m_path[self.enter_index - self.enter_sign])

        #switch enter and exit
        #self.facing = flip_facing(self.facing)

    def next_cell(self, direction, cell_id, turn_direction='c'):
        #direction will be used for going in reverse not supported atm
        if direction == 0:
            if self.m_path[cell_id] == self.exit:
                temp_p = self.lead_into_path[turn_direction]
                if temp_p == 0:
                    if DEBUG:
                        print('dono what do to, at end of path, yet path doesn\'t lead into anything')
                    return self.exit, self.exit_index, self
                else:


                    p = self.lead_into_path[turn_direction]
                    return p.enter, p.enter_index, p
            else:
                return self.m_path[cell_id+self.exit_sign], cell_id+self.exit_sign, self
        else:
            if self.m_path[cell_id] == self.enter:
                return self.enter, cell_id
            else:
                return self.m_path[cell_id+self.enter_sign], cell_id-self.enter_sign, self

    def at_intersection(self, cell):
        if cell == self.exit and self.exit_inter_cell != 0:
            #if man_hat(cell.x, cell.y, self.exit_inter_cell.x, self.exit_inter_cell.y) == 1:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Path):
            if self.id == other.id:
                return True
            else:
                return False
        else:
            return False


def man_hat(x1, y1, x2, y2):
    return int(math.fabs(x1 - x2) + math.fabs(y1 - y2))

#checks the orientation of celltwo relative to cellone
def get_facing(cellOne, cellTwo):
    if cellOne.x < cellTwo.x:
        if cellOne.y == cellTwo.y:
            return Path.EAST
    elif cellOne.x > cellTwo.x:
        if cellOne.y == cellTwo.y:
            return Path.WEST

    if cellOne.y < cellTwo.y:
        if cellOne.x == cellTwo.x:
            return Path.SOUTH
    elif cellOne.y > cellTwo.y:
        if cellOne.x == cellTwo.x:
            return Path.NORTH
    return -1


def flip_facing(d):
    if d == Path.NORTH:
        return Path.SOUTH
    elif d == Path.SOUTH:
        return Path.NORTH
    elif d == Path.WEST:
        return Path.EAST
    elif d == Path.EAST:
        return Path.WEST
    return -1


class Intersection:
    next_id = 0

    def __init__(self, x, y, file_id=-1):
        if file_id != -1:
            self.id = file_id
        else:
            self.id = Intersection.next_id
            Intersection.next_id += 1
        self.m_enter_exits = {}
        self.incoming_paths = {}
        self.outgoing_paths = {}
        self.traffic_lights = {}
        self.body = {}
        self.coord = Coord(x, y)
        self.body_info = {}
        self.set_body()

    def set_body(self):
        pass


class Two_by_Two(Intersection):
    #coord is the upper left cell
    def __init__(self, x, y):
        Intersection.__init__(self, x, y)

    def add_body_cell(self, i, c):
        self.body[i] = c
        self.num_body_cells = len(self.body)
        c.total_length = c.total_width

    def set_body(self):
        #body goes counter-clockwise starting in the lower right
        self.add_body_cell(0, Cell(self.coord.x+1, self.coord.y+1))
        self.add_body_cell(1, Cell(self.coord.x+1, self.coord.y))
        self.add_body_cell(2, Cell(self.coord.x, self.coord.y))
        self.add_body_cell(3, Cell(self.coord.x, self.coord.y+1))

        self.body_info[0] = (self.body[0].x, self.body[0].y+1, 'enter')
        self.body_info[1] = (self.body[1].x+1, self.body[1].y, 'enter')
        self.body_info[2] = (self.body[2].x, self.body[2].y-1, 'enter')
        self.body_info[3] = (self.body[3].x-1, self.body[3].y, 'enter')

        self.body_info[4] = (self.body[0].x+1, self.body[0].y, 'exit')
        self.body_info[5] = (self.body[1].x, self.body[1].y-1, 'exit')
        self.body_info[6] = (self.body[2].x-1, self.body[2].y, 'exit')
        self.body_info[7] = (self.body[3].x, self.body[3].y+1, 'exit')

        p = Path(0)
        p.add_Cell(self.body[0])
        self.m_enter_exits[(0, 'right')] = p

        p = Path(0)
        p.add_Cell(self.body[0])
        p.add_Cell(self.body[1])
        self.m_enter_exits[(0, 'straight')] = p

        p = Path(0)
        p.add_Cell(self.body[0])
        p.add_Cell(self.body[1])
        p.add_Cell(self.body[2])
        self.m_enter_exits[(0, 'left')] = p

        p = Path(0)
        p.add_Cell(self.body[1])
        self.m_enter_exits[(1, 'right')] = p

        p = Path(0)
        p.add_Cell(self.body[1])
        p.add_Cell(self.body[2])
        self.m_enter_exits[(1, 'straight')] = p

        p = Path(0)
        p.add_Cell(self.body[1])
        p.add_Cell(self.body[2])
        p.add_Cell(self.body[3])
        self.m_enter_exits[(1, 'left')] = p

        p = Path(0)
        p.add_Cell(self.body[2])
        self.m_enter_exits[(2, 'right')] = p

        p = Path(0)
        p.add_Cell(self.body[2])
        p.add_Cell(self.body[3])
        self.m_enter_exits[(2, 'straight')] = p

        p = Path(0)
        p.add_Cell(self.body[2])
        p.add_Cell(self.body[3])
        p.add_Cell(self.body[0])
        self.m_enter_exits[(2, 'left')] = p

        p = Path(0)
        p.add_Cell(self.body[3])
        self.m_enter_exits[(3, 'right')] = p

        p = Path(0)
        p.add_Cell(self.body[3])
        p.add_Cell(self.body[0])
        self.m_enter_exits[(3, 'straight')] = p

        p = Path(0)
        p.add_Cell(self.body[3])
        p.add_Cell(self.body[0])
        p.add_Cell(self.body[1])
        self.m_enter_exits[(3, 'left')] = p

        #for j in ['right', 'straight', 'left']:
        #    for i in range(4):
        #        p = Path(0)
        #        if j == 'right' or j == 'straight' or j == 'left':
        #            p.add_Cell(self.body[i])
        #        elif j == 'straight' or j == 'left':
        #            p.add_Cell(self.body[(i+1)%4])
        #        elif j == 'left':
        #            p.add_Cell(self.body[(i+2)%4])
        #        self.m_enter_exits[(i, j)] = p
        self.traffic_lights[0] = TrafficLight()
        self.traffic_lights[1] = TrafficLight()
        self.traffic_lights[2] = TrafficLight()
        self.traffic_lights[3] = TrafficLight()

    def path_overlap(self, p):
        for c in self.body.values():
            if man_hat(c.x, c.y, p.enter.x, p.enter.y) == 0 or man_hat(c.x, c.y, p.exit.x, p.exit.y) == 0:
                return True
        return False

    def add_paths(self, path_list):
        t_list = [False for _ in path_list]
        for t, p in enumerate(path_list):
            t_list[t] = self.add_path(p)
        return t_list

    def contains_path(self, p):
        in_paths = [i for i in self.incoming_paths.values()]
        out_paths = [i for i in self.outgoing_paths.values()]
        for i in in_paths + out_paths:
            if p == i:
                return True
        return False

    def add_path(self, p, switch=True):

        if DEBUG and (p.exit is None or p.enter is None):
            print('something is NONE D: ')
            return False

        if self.path_overlap(p):
            if DEBUG:
                print('path is overlapping')
            return False

        #if len(self.outgoing_paths) + len(self.incoming_paths) == 8:
        #    if DEBUG:
        #        print('full atm remove a path or ya.....')

        if self.contains_path(p):
            if DEBUG:
                print('already contains path')
            return False

        if switch:
            #can be improved but i like it this way D : i am conflicted
            body_value = -1
            next_to = False
            _enter = False
            _exit = False
            coords = None

            for c, d in zip(self.body_info.keys(), self.body_info.values()):
                if man_hat(d[0], d[1], p.enter.x, p.enter.y) == 0 or man_hat(d[0], d[1], p.exit.x, p.exit.y) == 0:
                    coords = d[0], d[1]
                    body_value = c % self.num_body_cells
                    next_to = True
                    if d[2] == 'enter':
                        _enter = True
                    elif d[2] == 'exit':
                        _exit = True
                    else:
                        if DEBUG:
                            print('something wrong! which is it? enter or exit? path.py')
                            return False
                    break

            if next_to:
                if _enter:
                    if man_hat(coords[0], coords[1], p.exit.x, p.exit.y) == 0:
                        self.add_path_helper(p, body_value, 'enter')
                    else:
                        p.switch_direction()
                        if man_hat(coords[0], coords[1], p.exit.x, p.exit.y) == 0:
                            self.add_path_helper(p, body_value, 'enter')
                        else:
                            if DEBUG:
                                print('error after switch enter')
                elif _exit:
                    if man_hat(coords[0], coords[1], p.enter.x, p.enter.y) == 0:
                        self.add_path_helper(p, body_value, 'exit')
                    else:
                        p.switch_direction()
                        if man_hat(coords[0], coords[1], p.enter.x, p.enter.y) == 0:
                            self.add_path_helper(p, body_value, 'exit')
                        else:
                            if DEBUG:
                                print('error after switch exit')
                return True
            else:
                if DEBUG:
                    messg = 'path ' + repr(p.id) + ' is not near intersection ' + repr(self.id)
                    print(messg)
                return False
        else:
            if DEBUG:
                print('not implemented atm')
            return False

    def add_path_helper(self, p, c, d):
        if d == 'enter':
            self.incoming_paths[c] = p
            p.exit_inter_cell = 1
            for j in ['right', 'straight', 'left']:
                p.lead_into_path[j] = self.m_enter_exits[(c, j)]

            self.traffic_lights[c].set_cell(p.exit)
        elif d == 'exit':
            self.outgoing_paths[c] = p
            p.enter_inter_cell = 1
            temp = self.m_enter_exits[(c, 'right')]
            temp.lead_into_path['c'] = p
            d = get_facing(temp.exit, p.enter)
            if d != -1:
                temp.c_facing[temp.exit_index] = d

            temp = self.m_enter_exits[((c+2) % 4, 'left')]
            temp.lead_into_path['c'] = p
            d = get_facing(temp.exit, p.enter)
            if d != -1:
                temp.c_facing[temp.exit_index] = d

            temp = self.m_enter_exits[((c+3) % 4, 'straight')]
            temp.lead_into_path['c'] = p
            d = get_facing(temp.exit, p.enter)
            if d != -1:
                temp.c_facing[temp.exit_index] = d

    def add_incoming_path(self, p):
        if DEBUG and p.exit is None:
            print('p.exit is None')
            return False
        for c in self.body.keys():
            if man_hat(self.body[c].x, self.body[c].y, p.exit.x, p.exit.y) == 1:
                self.incoming_paths[c] = p
                p.exit_inter_cell = 1
                for j in ['right', 'left', 'straight']:
                    #self.m_enter_exits[(c, j)].set_enter(p.exit)
                    p.lead_into_path[j] = self.m_enter_exits[(c, j)]

                if DEBUG:
                    print('added incoming path')
                return True
        if DEBUG:
            print('did not add incoming path')
        return False

    def add_outgoing_path(self, p):
        if DEBUG and p.enter is None:
            print('p.enter is None')
            return False

        for c in self.body.keys():
            if man_hat(self.body[c].x, self.body[c].y, p.enter.x, p.enter.y) == 1:
                self.outgoing_paths[c] = p
                p.enter_inter_cell = 1

                #self.m_enter_exits[(c, 'right')].set_exit(p.enter)
                #self.m_enter_exits[((c+2)%4, 'left')].set_exit(p.enter)
                #self.m_enter_exits[((c+3)%4, 'straight')].set_exit(p.enter)

                self.m_enter_exits[(c, 'right')].lead_into_path['c'] = p
                self.m_enter_exits[((c+2)%4, 'left')].lead_into_path['c'] = p
                self.m_enter_exits[((c+3)%4, 'straight')].lead_into_path['c'] = p

                #for j in ['right', 'left', 'straight']:
                #    for k in range(4):
                #        temp_c = self.m_enter_exits[(k, j)]
                #        if man_hat(temp_c.x, temp_c.y, p.enter.x, p.enter.y) == 1:
                #            self.m_enter_exits[(c, j)].set_exit(p.enter)
                #            break
                if DEBUG:
                    print('added outgoing path')
                return True
        if DEBUG:
            print('did not add outgoing path')
        return False


class Coord:
    #possible of making a hard decision of one coord
    #for each x,y tuple
    def __init__(self, x, y):
        if type(x) is not int:
            print('some coords are not ints\n')

        self.x = int(x)
        self.y = int(y)


class Cell(Coord):
    next_id = 0

    def __init__(self, x, y):
        Coord.__init__(self, x, y)
        self.id = Cell.next_id
        Cell.next_id += 1
        self.road_type = 0
        self.contains_stoplight = False
        self.stoplight = 'green'
        self.occupied = False
        #currently in feet
        self.total_length = 5280
        self.total_width = 12

    def set_stoplight(self, t):
        self.contains_stoplight = t

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.id == other.id:
            return True
        else:
            return False


def sign(x):
    if x == 0:
        return 0
    return int(math.copysign(1, x))