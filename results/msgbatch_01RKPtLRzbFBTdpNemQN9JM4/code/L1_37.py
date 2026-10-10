import cadquery as cq
import math

# Disc: diameter 80, thickness 15, along Z from 0 to 15
disc = cq.Workplane("XY").circle(40).extrude(15)

# Cross slots: 10 wide, 5 deep from top surface (z=10 to 15), extending through to edge
slot_x = cq.Workplane("XY").workplane(offset=10).rect(90, 10).extrude(5)
slot_y = cq.Workplane("XY").workplane(offset=10).rect(10, 90).extrude(5)

result = disc.cut(slot_x).cut(slot_y)
