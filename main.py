__author__ = 'elemental'

# This project is using python v3

from universe import Universe
from world import World
from path import *
from car import Car
from road import *

w = World(20, 20)

i1 = Two_by_Two(2, 2)
i2 = Two_by_Two(13, 2)
i3 = Two_by_Two(13, 14)
i4 = Two_by_Two(2, 14)

r1 = Two_Lane_Road(i1, i2)
r2 = Two_Lane_Road(i2, i3)
r3 = Two_Lane_Road(i3, i4)
r4 = Two_Lane_Road(i4, i1)

w.add_roads([r1, r2, r3, r4])
w.add_intersections([i1, i2, i3, i4])

c = Car(r1.paths[1], w)
d = Car(r1.paths[0], w, 'left')
e = Car(r2.paths[0], w)

u = Universe(w)
u.start()