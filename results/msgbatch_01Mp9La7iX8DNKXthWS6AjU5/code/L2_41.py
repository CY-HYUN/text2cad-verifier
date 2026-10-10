import cadquery as cq
import math

R = 20.0
H = 60.0

# Octagonal prism (circumscribed diameter 40)
body = cq.Workplane("XY").polygon(8, 2 * R).extrude(H)

# Top sharpening cut: triangle profile in XZ plane, revolved about Z axis
tri = (
    cq.Workplane("XZ")
    .polyline([(R + 1, H + 1), (R + 1, H - (R + 1) + 1 - 1 + 0), (0, H)])
    .close()
)
# Build precise triangle along 45-degree line from (0,H) to (R,H-R), extended outward
tri = (
    cq.Workplane("XZ")
    .polyline([(0, H), (R + 2, H - (R + 2)), (R + 2, H + 2), (0, H + 2)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(tri)

# Annular groove at mid height: 5 tall, 2 deep from outer vertex radius
groove = (
    cq.Workplane("XZ")
    .polyline([(R - 2, H / 2 - 2.5), (R + 1, H / 2 - 2.5),
               (R + 1, H / 2 + 2.5), (R - 2, H / 2 + 2.5)])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
body = body.cut(groove)

result = body
