import cadquery as cq
import math

# Central pillar
pillar = cq.Workplane("XY").circle(10).extrude(100)

# Sector step profile
r1, r2 = 5.0, 25.0
a = math.radians(30)
h = a / 2

step = (
    cq.Workplane("XY")
    .moveTo(r1, 0)
    .lineTo(r2, 0)
    .threePointArc((r2 * math.cos(h), r2 * math.sin(h)),
                   (r2 * math.cos(a), r2 * math.sin(a)))
    .lineTo(r1 * math.cos(a), r1 * math.sin(a))
    .threePointArc((r1 * math.cos(h), r1 * math.sin(h)), (r1, 0))
    .close()
    .extrude(5)
)

result = pillar
for i in range(10):
    inst = step.rotate((0, 0, 0), (0, 0, 1), 30 * i).translate((0, 0, 10 * i))
    result = result.union(inst)
