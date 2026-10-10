import cadquery as cq
import math

height = 20.0
r_cyl = 10.0
r_circle = 10.0

result = None
for i in range(6):
    a = math.radians(60 * i)
    x = r_circle * math.cos(a)
    y = r_circle * math.sin(a)
    c = cq.Workplane("XY").center(x, y).circle(r_cyl).extrude(height)
    result = c if result is None else result.union(c)
