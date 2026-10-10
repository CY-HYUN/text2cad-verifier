import cadquery as cq
import math

R = 50.0
d0, d1 = 30.0, 15.0
n = 12

wires = []
for i in range(n + 1):
    f = i / n
    t = math.radians(90.0 * f)
    r = (d0 + (d1 - d0) * f) / 2.0
    center = cq.Vector(R * math.cos(t), R * math.sin(t), 0)
    normal = cq.Vector(-math.sin(t), math.cos(t), 0)
    wires.append(cq.Wire.makeCircle(r, center, normal))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
