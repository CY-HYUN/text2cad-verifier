import cadquery as cq
import math

outer = cq.Workplane("XY").box(60, 60, 60)
cavity = cq.Workplane("XY").box(50, 50, 50)
shell = outer.cut(cavity)

core = cq.Workplane("XY").box(20, 20, 20)

result = shell.union(core)

# rods along each axis, from inner cube to wall (overlapping slightly)
length = 17.0  # from 9 to 26
center = (9 + 26) / 2.0
for sign in (1, -1):
    # Z axis
    rod = cq.Workplane("XY").workplane(offset=sign*center - length/2).circle(1.0).extrude(length)
    result = result.union(rod)
    # X axis
    rod = cq.Workplane("YZ").workplane(offset=sign*center - length/2).circle(1.0).extrude(length)
    result = result.union(rod)
    # Y axis
    rod = cq.Workplane("XZ").workplane(offset=-sign*center - length/2).circle(1.0).extrude(length)
    result = result.union(rod)
