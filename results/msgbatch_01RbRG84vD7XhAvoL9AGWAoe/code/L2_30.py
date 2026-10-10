import cadquery as cq

L, W, H = 60.0, 30.0, 30.0
r_long = 10.0   # semi-cylindrical cut along the long (X) axis
r_cross = 12.0  # cross arch so the block rests on four corner feet
hole_d = 6.0

body = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Semi-cylinder along the long axis on the bottom face
cut_long = (
    cq.Workplane("YZ")
    .circle(r_long)
    .extrude(L + 2)
    .translate((-(L + 2) / 2, 0, 0))
)
body = body.cut(cut_long)

# Cross arch along the short axis, leaving four corner contacts
cut_cross = (
    cq.Workplane("XZ")
    .circle(r_cross)
    .extrude(W + 2)
    .translate((0, (W + 2) / 2, 0))
)
body = body.cut(cut_cross)

# Vertical through-holes passing through the arch
holes = (
    cq.Workplane("XY")
    .pushPoints([(-20, 0), (20, 0)])
    .circle(hole_d / 2)
    .extrude(H + 2)
    .translate((0, 0, -1))
)
result = body.cut(holes)
