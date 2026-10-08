import cadquery as cq
import math

r = 10.0      # circle radius (diameter 20 mm)
R = 10.0      # distance of each circle centre from the origin
n = 6         # number of circles in the circular array
h = 20.0      # extrusion height

result = None
for i in range(n):
    a = 2 * math.pi * i / n
    c = (
        cq.Workplane("XY")
        .center(R * math.cos(a), R * math.sin(a))
        .circle(r)
        .extrude(h)
    )
    result = c if result is None else result.union(c)

# fill any tiny central gap (circles pass exactly through origin)
result = result.union(cq.Workplane("XY").circle(R * 0.5).extrude(h))
result = result.clean()
