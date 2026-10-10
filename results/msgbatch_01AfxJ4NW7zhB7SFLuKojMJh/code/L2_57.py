import cadquery as cq
import math

R = 50.0
T = 30.0

body = cq.Workplane("XY").circle(R).extrude(T)

# eight semicircular grooves: cylinders of radius 10 centered on the outer circumference
pts = [(R * math.cos(math.radians(45 * i)), R * math.sin(math.radians(45 * i))) for i in range(8)]
grooves = cq.Workplane("XY").pushPoints(pts).circle(10).extrude(T)
body = body.cut(grooves)

# central hole dia 30
hole = cq.Workplane("XY").circle(15).extrude(T)
body = body.cut(hole)

# keyway: width 8, depth 4 beyond the hole wall (along +X)
key = cq.Workplane("XY").center(15 + 2, 0).rect(4 + 0.0 + 4, 8).extrude(T)
# rect spans x from 13 to 21 -> cuts 6 mm beyond wall? adjust to exactly 4 mm depth
key = cq.Workplane("XY").center((14 + 19) / 2, 0).rect(5, 8).extrude(T)
body = body.cut(key)

result = body
