import cadquery as cq
import math

R = 50.0
r0 = 15.0   # 30 mm diameter at start
r1 = 7.5    # 15 mm diameter at end
n = 12

wires = []
for i in range(n + 1):
    f = i / n
    t = f * math.pi / 2
    r = r0 + (r1 - r0) * f
    center = cq.Vector(R * math.cos(t), R * math.sin(t), 0)
    tangent = cq.Vector(-math.sin(t), math.cos(t), 0)
    wires.append(cq.Wire.makeCircle(r, center, tangent))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
