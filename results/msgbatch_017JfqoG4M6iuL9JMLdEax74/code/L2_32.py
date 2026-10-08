import cadquery as cq
import math

cyl_d = 20.0
array_r = 10.0  # array circle diameter 20 mm
height = 20.0

result = None
for i in range(6):
    a = math.radians(60 * i)
    x, y = array_r * math.cos(a), array_r * math.sin(a)
    c = cq.Workplane("XY").center(x, y).circle(cyl_d / 2).extrude(height)
    result = c if result is None else result.union(c)

# fill any tiny central gap to ensure a single solid
core = cq.Workplane("XY").circle(array_r * 0.5).extrude(height)
result = result.union(core).clean()
