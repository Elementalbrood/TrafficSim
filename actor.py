__author__ = 'elemental'


class Actor():
    next_id = 0

    def __init__(self, cell=None, world=None):
        self.id = Actor.next_id
        Actor.next_id += 1
        self.cell = None
        self.world = None

        if cell is not None:
            self.cell = cell

        if world is not None:
            self.world = world
            self.world.add_actor(self)

        self.pos_x = 0
        self.pos_y = 0

    def set_cell(self, c):
        self.cell = c

    def set_world(self, w):
        self.world = w
        self.world.add_actor(w)

    def act(self, delta):
        pass

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False