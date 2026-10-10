import cadquery as cq
import math

s = 40.0
d = 10.0
cube = cq.Workplane("XY").box(s, s, s, centered=(True, True, False))
cz = (cq.Workplane("XY").workplane(offset=-1).circle(d/2).extrude(s+2))
cx = (cq.Workplane("YZ").workplane(offset=-s/2-1).center(0, s/2).circle(d/2).extrude(s+2))
cy = (cq.Workplane("XZ").workplane(offset=-s/2-1).center(0, s/2).circle(d/2).extrude(s+2))
result = cube.cut(cz).cut(cx).cut(cy)
