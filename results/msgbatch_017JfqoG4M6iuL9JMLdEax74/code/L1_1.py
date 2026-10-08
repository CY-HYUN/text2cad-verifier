import cadquery as cq
import math

af = 50.0  # across flats
d_circ = af / math.cos(math.radians(30))
h = 20.0

result = (
    cq.Workplane("XY")
    .polygon(6, d_circ)
    .extrude(h)
    .faces(">Z").edges()
    .chamfer(2.0)
    .faces(">Z").workplane()
    .hole(20.0)
)
