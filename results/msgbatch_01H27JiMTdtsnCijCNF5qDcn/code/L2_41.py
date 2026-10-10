import cadquery as cq
import math

R = 20.0
H = 60.0

body = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# top chamfer triangle (45 degrees), revolved cut about Z axis
d = 12.0
tri = (
    cq.Workplane("XZ")
    .polyline([(R + 1, H + 1), (R + 1, H - d - 1), (R - d, H + 1)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(tri)

# annular groove at mid-height
groove = (
    cq.Workplane("XZ")
    .polyline([(R - 2, H / 2 - 2.5), (R + 1, H / 2 - 2.5), (R + 1, H / 2 + 2.5), (R - 2, H / 2 + 2.5)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(groove)

result = body
