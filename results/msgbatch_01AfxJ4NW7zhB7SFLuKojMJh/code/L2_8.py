import cadquery as cq
import math

# Central column: diameter 20, height 100
column = cq.Workplane("XY").circle(10).extrude(100)

result = column

radius = 50.0
thickness = 5.0
sector_angle = 30.0
n_steps = 10
dz = 10.0
dtheta = 30.0

for i in range(n_steps):
    a0 = i * dtheta
    a1 = a0 + sector_angle
    am = a0 + sector_angle / 2.0
    z = i * dz
    p_start = (radius * math.cos(math.radians(a0)), radius * math.sin(math.radians(a0)))
    p_mid = (radius * math.cos(math.radians(am)), radius * math.sin(math.radians(am)))
    p_end = (radius * math.cos(math.radians(a1)), radius * math.sin(math.radians(a1)))
    step = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .moveTo(0, 0)
        .lineTo(*p_start)
        .threePointArc(p_mid, p_end)
        .close()
        .extrude(thickness)
    )
    result = result.union(step)
