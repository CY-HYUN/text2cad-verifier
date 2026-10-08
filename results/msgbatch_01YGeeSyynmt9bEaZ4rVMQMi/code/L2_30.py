import cadquery as cq

# Base prism 60 x 30 x 30 (X x Y x Z), bottom face on Z=0
L, W, H = 60.0, 30.0, 30.0
body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# Semi-elliptical arch at the center of the bottom edge (front view = XZ plane)
a, b = 20.0, 15.0  # semi-axes: horizontal half-width, arch height
arch = (
    cq.Workplane("XZ")
    .ellipse(a, b)          # centered on bottom edge; lower half lies outside the body
    .extrude(W / 2 + 1, both=True)
)
body = body.cut(arch)

# Circular through-cut from the center of the top face downward
hole_d = 10.0
hole = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .circle(hole_d / 2)
    .extrude(-H - 1)
)
body = body.cut(hole)

result = body
