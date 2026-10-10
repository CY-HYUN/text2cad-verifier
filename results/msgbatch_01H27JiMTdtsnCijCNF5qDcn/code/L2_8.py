import cadquery as cq
import math

pillar = cq.Workplane("XY").circle(10).extrude(100)

r_in, r_out = 5.0, 25.0
a = math.radians(30)
m = a / 2

def pt(r, ang):
    return (r * math.cos(ang), r * math.sin(ang))

step = (
    cq.Workplane("XY")
    .moveTo(*pt(r_in, 0))
    .lineTo(*pt(r_out, 0))
    .threePointArc(pt(r_out, m), pt(r_out, a))
    .lineTo(*pt(r_in, a))
    .threePointArc(pt(r_in, m), pt(r_in, 0))
    .close()
    .extrude(5)
)

result = pillar
for i in range(10):
    s = step.rotate((0, 0, 0), (0, 0, 1), 30 * i).translate((0, 0, 10 * i))
    result = result.union(s)
