import cadquery as cq
import math

body = cq.Workplane("XY").circle(15).extrude(50)

# Hexagon: 15 mm across flats -> circumscribed diameter = 15 / cos(30°)
hex_d = 15 / math.cos(math.radians(30))
hex_cut = (cq.Workplane("XY").workplane(offset=25)
           .polygon(6, hex_d).extrude(25))

# Round hole: 15 mm diameter from bottom up 25 mm
circ_cut = cq.Workplane("XY").circle(7.5).extrude(25)

result = body.cut(hex_cut).cut(circ_cut)
