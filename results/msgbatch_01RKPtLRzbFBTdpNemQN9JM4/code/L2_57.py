import cadquery as cq
import math

R = 50.0
T = 30.0
groove_r = 10.0
n = 8

body = cq.Workplane("XY").circle(R).extrude(T)

# Eight grooves, axes parallel to the main axis, centered on the outer circumference
pts = [(R * math.cos(2 * math.pi * i / n), R * math.sin(2 * math.pi * i / n)) for i in range(n)]
grooves = cq.Workplane("XY").pushPoints(pts).circle(groove_r).extrude(T)
body = body.cut(grooves)

# Central hole
hole = cq.Workplane("XY").circle(15.0).extrude(T)
body = body.cut(hole)

# Keyway: width 8, depth 4 beyond the hole wall (radially from r=15 to r=19)
key = (cq.Workplane("XY")
       .center(0, 15.0 + 4.0 / 2.0 - 0.0)
       .rect(8.0, 4.0 + 0.0)
       .extrude(T))
# extend slightly into the hole to ensure clean cut
key = key.union(cq.Workplane("XY").center(0, 15.0).rect(8.0, 2.0).extrude(T))
body = body.cut(key)

result = body
