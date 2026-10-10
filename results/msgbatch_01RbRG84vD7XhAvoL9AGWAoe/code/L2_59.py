import cadquery as cq

L = 50.0
d = 15.0
depth = 30.0

# 50 mm cube centred at the origin
cube = cq.Workplane("XY").box(L, L, L)

# Blind hole along X, entering from the +X face, 30 mm deep
hole_x = (
    cq.Workplane("YZ")
    .workplane(offset=L / 2 - depth)
    .circle(d / 2)
    .extrude(depth)
)

# Blind hole along Z, entering from the +Z face, 30 mm deep
hole_z = (
    cq.Workplane("XY")
    .workplane(offset=L / 2 - depth)
    .circle(d / 2)
    .extrude(depth)
)

result = cube.cut(hole_x).cut(hole_z)
