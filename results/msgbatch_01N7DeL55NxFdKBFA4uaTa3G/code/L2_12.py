import cadquery as cq
import math

# Base: 100mm diameter, 10mm thick
base = cq.Workplane("XY").circle(50).extrude(10)

# Frustum parameters
pattern_r = 30.0      # radius of circular pattern
h_frustum = 15.0      # height from base top to reference plane
r_bottom = 10.0       # 20mm diameter
r_top = 5.0           # 10mm diameter

result = base
for i in range(3):
    ang = math.radians(i * 120)
    x = pattern_r * math.cos(ang)
    y = pattern_r * math.sin(ang)
    frustum = (
        cq.Workplane("XY")
        .workplane(offset=10)
        .center(x, y)
        .circle(r_bottom)
        .workplane(offset=h_frustum)
        .circle(r_top)
        .loft(combine=True)
    )
    result = result.union(frustum)

# Through holes 5mm diameter at center of each frustum
for i in range(3):
    ang = math.radians(i * 120)
    x = pattern_r * math.cos(ang)
    y = pattern_r * math.sin(ang)
    hole = (
        cq.Workplane("XY")
        .workplane(offset=-1)
        .center(x, y)
        .circle(2.5)
        .extrude(10 + h_frustum + 2)
    )
    result = result.cut(hole)
