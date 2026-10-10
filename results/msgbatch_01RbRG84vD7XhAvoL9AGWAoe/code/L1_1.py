import cadquery as cq
import math

af = 50.0
d_circ = af / math.cos(math.radians(30))
h = 20.0

body = cq.Workplane("XY").polygon(6, d_circ).extrude(h)
body = body.faces(">Z").edges().chamfer(2.0)
result = body.faces(">Z").workplane().hole(20.0)
