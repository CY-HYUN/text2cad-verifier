import cadquery as cq
import math

# Shaft: circle dia 40 on XY, extruded 80 along Z
shaft = cq.Workplane("XY").circle(20.0).extrude(80.0)

# Keyway cutter: box on plane y=20 (parallel to XZ), 10 wide in X, 80 long in Z,
# cut 5 mm in -Y direction (from y=20 to y=15)
cutter = (
    cq.Workplane("XY")
    .box(10.0, 5.0, 80.0, centered=(True, False, False))
    .translate((0, 15.0, 0))
)

result = shaft.cut(cutter)
