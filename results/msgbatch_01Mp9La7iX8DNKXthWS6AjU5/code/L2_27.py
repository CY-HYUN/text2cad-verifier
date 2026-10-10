import cadquery as cq
import math

# Base cylinder: diameter 30, length 50 (z = 0 to 50)
body = cq.Workplane("XY").circle(15).extrude(50)

# Top hexagonal pocket: across flats 15 mm -> circumscribed diameter = 15 / cos(30 deg)
hex_d = 15 / math.cos(math.radians(30))
hex_cut = (
    cq.Workplane("XY").workplane(offset=25)
    .polygon(6, hex_d)
    .extrude(25)
)

# Bottom circular hole: diameter 15, 25 mm deep (z = 0 to 25)
hole_cut = cq.Workplane("XY").circle(7.5).extrude(25)

result = body.cut(hex_cut).cut(hole_cut)
