__author__ = 'elemental'

from path import *


class Road:
    def __init__(self):

        self.paths = {}


class Two_Lane_Road(Road):
    def __init__(self, TTOne=None, TTTwo=None):
        Road.__init__(self)
        if isinstance(TTOne, Two_by_Two) and isinstance(TTTwo, Two_by_Two):
            self.set_between_inter(TTOne, TTTwo)

    def clear_road(self):
        self.paths = {}

    def set_between_inter(self, interOne, interTwo):
        if not (isinstance(interOne, Two_by_Two) and isinstance(interTwo, Two_by_Two)):
            print('intersections are not 2 by 2s')
            return False

        x1 = interOne.coord.x
        y1 = interOne.coord.y
        x2 = interTwo.coord.x
        y2 = interTwo.coord.y
        if not (x1 == x2 or y1 == y2):
            print('intersections are not lined up')
            return False

        b1 = None
        b2 = None
        b3 = None
        b4 = None

        if x1 == x2:
            c = 2*man_hat(x1, y1, x2, y2)

            for i in interOne.body.values():
                if i.x != x1:
                    continue
                for j in interTwo.body.values():
                    if j.x != x2:
                        continue
                    temp = man_hat(i.x, i.y, j.x, j.y)
                    if temp < c:
                        c = temp
                        b1 = i
                        b2 = j

            for i in interOne.body.values():
                if i.y != b1.y:
                    continue
                for j in interTwo.body.values():
                    if j.y != b2.y:
                        continue
                    if man_hat(i.x, i.y, j.x, j.y) == c and i != b1 and j != b2:
                        b3 = i
                        b4 = j

        elif y1 == y2:
            c = 2*man_hat(x1, y1, x2, y2)

            for i in interOne.body.values():
                if i.y != y1:
                    continue
                for j in interTwo.body.values():
                    if j.y != y2:
                        continue
                    temp = man_hat(i.x, i.y, j.x, j.y)
                    if temp < c:
                        c = temp
                        b1 = i
                        b2 = j

            for i in interOne.body.values():
                if i.x != b1.x:
                    continue
                for j in interTwo.body.values():
                    if j.x != b2.x:
                        continue
                    if man_hat(i.x, i.y, j.x, j.y) == c and i != b1 and j != b2:
                        b3 = i
                        b4 = j

        self.clear_road()

        self.paths[0] = Path()
        self.paths[1] = Path()

        dir_x = sign(b1.x - b2.x) * -1
        dir_y = sign(b1.y - b2.y) * -1

        if dir_x == 0:
            i = b1.y + dir_y
            while i != b2.y:
                self.add_y_segment(i, b1.x, b3.x)
                i += dir_y

        elif dir_y == 0:
            i = b1.x + dir_x

            while i != b2.x:
                self.add_x_segment(i, b1.y, b3.y)
                i += dir_x

        interOne.add_path(self.paths[0])
        interOne.add_path(self.paths[1])
        interTwo.add_path(self.paths[0])
        interTwo.add_path(self.paths[1])

    def add_x_segment(self, x, y1, y2):
        self.paths[0].add_cell(x, y1)
        self.paths[1].add_cell(x, y2)

    def add_y_segment(self, y, x1, x2):
        self.paths[0].add_cell(x1, y)
        self.paths[1].add_cell(x2, y)

def path_hat(p, x, y):
    if man_hat(p.enter.x, p.enter.y, x, y) == 1:
        return 0, True
    elif man_hat(p.exit.x, p.exit.y, x, y) == 1:
        return 1, True
    return False