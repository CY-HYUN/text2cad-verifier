import cadquery as cq

L, W, H = 60.0, 30.0, 30.0

# Main block, sitting on the ground (z = 0 is the bottom face)
body = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Semi-cylindrical cut along the long (X) axis on the bottom face
r_long = 10.0
cut_long = (
    cq.Workplane("YZ")
    .circle(r_long)
    .extrude(L + 2)
    .translate((-(L + 2) / 2, 0, 0))
)
body = body.cut(cut_long)

# Arch across the short axis, so the block only touches the ground at its four corners
r_cross = 18.0
cut_cross = (
    cq.Workplane("XZ")
    .circle(r_cross)
    .extrude(W + 2, both=True)
)
body = body.cut(cut_cross)

# Vertical holes drilled through the arch
holes = (
    cq.Workplane("XY")
    .pushPoints([(-20, 0), (20, 0), (0, 0)])
    .circle(3.0)
    .extrude(H + 2)
    .translate((0, 0, -1))
)
body = body.cut(holes)

result = body
