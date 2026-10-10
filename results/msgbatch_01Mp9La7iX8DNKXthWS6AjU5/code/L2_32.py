import cadquery as cq
import math

height = 30.0
r = 10.0      # circle radius (diameter 20)
offset = 10.0 # circle center distance from origin
n = 6

result = None
for i in range(n):
    a = math.radians(360.0 / n * i)
    x = offset * math.cos(a)
    y = offset * math.sin(a)
    cyl = cq.Workplane("XY").center(x, y).circle(r).extrude(height)
    result = cyl if result is None else result.union(cyl)

result = result.clean()
