import cadquery as cq
import math

h = 30
R = 10
result = None
for i in range(6):
    a = math.radians(60 * i)
    c = cq.Workplane("XY").center(R * math.cos(a), R * math.sin(a)).circle(10).extrude(h)
    result = c if result is None else result.union(c)
