import cadquery as cq
import math

OD = 30.0
L = 50.0
hex_depth = 25.0
round_depth = 25.0
inscribed = 15.0
circ_d = inscribed / math.cos(math.radians(30))  # circumscribed diameter
round_d = 15.0

body = cq.Workplane("XY").circle(OD / 2).extrude(L)

hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=L - hex_depth)
    .polygon(6, circ_d)
    .extrude(hex_depth)
)
round_cut = cq.Workplane("XY").circle(round_d / 2).extrude(round_depth)

result = body.cut(hex_cut).cut(round_cut)
