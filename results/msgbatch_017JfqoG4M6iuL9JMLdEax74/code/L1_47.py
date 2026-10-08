import cadquery as cq

# Shaft body: diameter 40 mm, length 80 mm along Z
shaft = cq.Workplane("XY").circle(20).extrude(80)

# Track-shaped keyway: 40 mm long along Z, 10 mm wide in Y, 5 mm deep from the +X surface
key = (
    cq.Workplane("YZ", origin=(15, 0, 40))
    .slot2D(40, 10, angle=90)
    .extrude(10)
)

result = shaft.cut(key)
