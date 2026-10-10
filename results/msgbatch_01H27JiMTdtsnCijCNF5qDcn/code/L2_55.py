import cadquery as cq
import math

R = 50.0
r_start = 15.0
r_end = 7.5
n = 12

wires = []
for i in range(n + 1):
    f = i / n
    t = math.radians(90.0 * f)
    center = cq.Vector(R * math.cos(t), 0, R * math.sin(t))
    tangent = cq.Vector(-math.sin(t), 0, math.cos(t))
    r = r_start + (r_end - r_start) * f
    wires.append(cq.Wire.makeCircle(r, center, tangent))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
