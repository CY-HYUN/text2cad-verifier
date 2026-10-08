import cadquery as cq
import math

L = 50.0
cube = cq.Workplane("XY").box(L, L, L)

# Diagonal direction between opposite vertices (-25,-25,-25) -> (25,25,25)
d = cq.Vector(1, 1, 1).normalized()
length = 200.0
start = cq.Vector(0, 0, 0) - d * (length / 2)

# Circle of diameter 10 on a plane perpendicular to the diagonal, extruded through
plane = cq.Plane(origin=start, xDir=cq.Vector(1, -1, 0).normalized(), normal=d)
cutter = cq.Workplane(plane).circle(5.0).extrude(length)

result = cube.cut(cutter)
