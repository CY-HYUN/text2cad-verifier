import cadquery as cq
import math

D = 30.0
L = 50.0
hex_flat = 15.0  # inscribed circle diameter (across flats)
hex_circ = hex_flat / math.cos(math.pi / 6)  # circumscribed diameter
hole_d = 15.0
depth = 25.0

body = cq.Workplane("XY").circle(D / 2).extrude(L)

hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=L - depth)
    .polygon(6, hex_circ)
    .extrude(depth)
)

round_cut = cq.Workplane("XY").circle(hole_d / 2).extrude(depth)

result = body.cut(hex_cut).cut(round_cut)
