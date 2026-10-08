import cadquery as cq

# Shaft: diameter 40 mm, length 80 mm along +Z
shaft = cq.Workplane("XY").circle(20.0).extrude(80.0)

# Keyway: 10 mm wide in X, full 80 mm length in Z, cut 5 mm deep from the y=+20 tangent plane
keyway = (
    cq.Workplane("XY")
    .box(10.0, 5.0, 80.0, centered=(True, False, False))
    .translate((0, 15.0, 0))
)

result = shaft.cut(keyway)
