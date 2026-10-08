import cadquery as cq
import math

# Main cylinder: D30 x L50
cyl = cq.Workplane("XY").circle(15).extrude(50)

# Hexagon: inscribed circle diameter 15 -> circumscribed diameter
hex_across_flats = 15.0
hex_circ_d = hex_across_flats / math.cos(math.radians(30))

# Hex pocket from top, 25 mm deep
hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=25)
    .polygon(6, hex_circ_d)
    .extrude(25)
)

# Round hole from bottom, D15, 25 mm deep (meets hex pocket)
round_cut = cq.Workplane("XY").circle(7.5).extrude(25)

result = cyl.cut(hex_cut).cut(round_cut)
