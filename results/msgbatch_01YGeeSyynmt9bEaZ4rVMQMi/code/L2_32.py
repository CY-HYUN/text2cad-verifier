import cadquery as cq
import math

r = 10.0      # circle radius (diameter 20 mm)
d = 10.0      # distance of each circle centre from the origin
n = 6
height = 20.0

result = None
for i in range(n):
    a = 2 * math.pi * i / n
    cyl = (cq.Workplane("XY")
           .center(d * math.cos(a), d * math.sin(a))
           .circle(r)
           .extrude(height))
    result = cyl if result is None else result.union(cyl)

result = result.clean()
