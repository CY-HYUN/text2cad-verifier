import cadquery as cq
import math

# Cylinder: diameter 40, height 40
cyl = cq.Workplane("XY").circle(20.0).extrude(40.0)

# Conical pit: triangular profile on XZ plane revolved 360 deg about Z
# Top radius 15 at z=40, apex at depth 15 (z=25)
profile = (
    cq.Workplane("XZ")
    .polyline([(0, 40.0), (15.0, 40.0), (0, 25.0)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

result = cyl.cut(profile)
