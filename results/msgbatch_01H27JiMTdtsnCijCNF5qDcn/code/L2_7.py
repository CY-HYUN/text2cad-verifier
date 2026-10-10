import cadquery as cq
import math

h = 15
circle = cq.Workplane("XY").circle(30).extrude(h)
rect = cq.Workplane("XY").center(40, 0).rect(80, 20).extrude(h)
body = circle.union(rect)

# large hole on top face
body = body.cut(
    cq.Workplane("XY").workplane(offset=h).center(5, 0).circle(15).extrude(-h)
)

# small hole at the center of the rod end
body = body.cut(
    cq.Workplane("XY").workplane(offset=h).center(70, 0).circle(5).extrude(-h)
)

result = body
