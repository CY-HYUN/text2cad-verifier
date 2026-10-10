import cadquery as cq
import math

h = 30.0
result = None
for i in range(6):
    a = math.radians(60 * i)
    c = (cq.Workplane("XY")
         .center(10 * math.cos(a), 10 * math.sin(a))
         .circle(10)
         .extrude(h))
    result = c if result is None else result.union(c)
