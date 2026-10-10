import cadquery as cq
import math

cyl_d = 20.0
array_d = 20.0
height = 20.0
n = 6

r = array_d / 2.0
result = None
for i in range(n):
    a = 2 * math.pi * i / n
    c = cq.Workplane("XY").center(r * math.cos(a), r * math.sin(a)).circle(cyl_d / 2.0).extrude(height)
    result = c if result is None else result.union(c)

# fill any tiny central gap
result = result.union(cq.Workplane("XY").circle(r).extrude(height))
