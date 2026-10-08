import cadquery as cq
import math

# Central pillar
pillar = cq.Workplane("XY").circle(10).extrude(100)

# Sector step profile
r_in, r_out, ang = 5.0, 25.0, 30.0
a = math.radians(ang)
am = a / 2

step = (
    cq.Workplane("XY")
    .moveTo(r_in, 0)
    .lineTo(r_out, 0)
    .threePointArc((r_out * math.cos(am), r_out * math.sin(am)),
                   (r_out * math.cos(a), r_out * math.sin(a)))
    .lineTo(r_in * math.cos(a), r_in * math.sin(a))
    .threePointArc((r_in * math.cos(am), r_in * math.sin(am)), (r_in, 0))
    .close()
    .extrude(5)
)

result = pillar
for i in range(10):
    inst = step.rotate((0, 0, 0), (0, 0, 1), 30 * i).translate((0, 0, 10 * i))
    result = result.union(inst)
