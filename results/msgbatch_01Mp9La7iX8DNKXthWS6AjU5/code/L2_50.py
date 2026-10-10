import cadquery as cq
import math

# stepped shaft profile (x along axis, y radius), revolved about X axis
pts = [
    (0, 0), (0, 10), (30, 10), (30, 15), (70, 15), (70, 10), (100, 10), (100, 0)
]
shaft = (cq.Workplane("XY").polyline(pts).close()
         .revolve(360, (0, 0, 0), (1, 0, 0)))

# groove on tangent plane at top of middle cylinder (z=15), cut 3.5 mm inward
groove = (cq.Workplane("XY").workplane(offset=15)
          .center(50, 0).rect(20, 6).extrude(-3.5))
shaft = shaft.cut(groove)

# end holes, dia 5, depth 10
left_hole = (cq.Workplane("YZ").circle(2.5).extrude(10))
right_hole = (cq.Workplane("YZ").workplane(offset=90).circle(2.5).extrude(10))
shaft = shaft.cut(left_hole).cut(right_hole)

result = shaft
