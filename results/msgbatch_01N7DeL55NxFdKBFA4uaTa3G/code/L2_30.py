import cadquery as cq

# Base rectangular prism 60 x 30 x 30 (bottom at z=0)
L, W, H = 60.0, 30.0, 30.0
body = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Semi-elliptical arch at the center of the bottom edge (front view XZ plane)
a, b = 20.0, 12.0  # horizontal / vertical semi-axes
arch = (
    cq.Workplane("XZ")
    .ellipse(a, b)          # centered on bottom edge -> upper half lies in the body
    .extrude(W, both=True)  # cut through front to back
)
body = body.cut(arch)

# Circular hole from the center of the top face, cut fully downward
hole_d = 10.0
hole = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .circle(hole_d / 2)
    .extrude(-H - 1)
)
body = body.cut(hole)

result = body
