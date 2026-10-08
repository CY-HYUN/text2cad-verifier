import cadquery as cq
import math

OD = 30.0
L = 50.0
seg = 25.0
flat = 15.0  # hexagon across-flats (inscribed circle diameter)
hex_circ = flat / math.cos(math.radians(30))  # circumscribed diameter ~17.32
d_round = 15.0

body = cq.Workplane("XY").circle(OD / 2).extrude(L)

# Lower circular hole (z = 0..25)
round_hole = cq.Workplane("XY").circle(d_round / 2).extrude(seg)

# Upper hexagonal hole (z = 25..50)
hex_hole = (
    cq.Workplane("XY")
    .workplane(offset=seg)
    .polygon(6, hex_circ)
    .extrude(seg)
)

result = body.cut(round_hole).cut(hex_hole)
