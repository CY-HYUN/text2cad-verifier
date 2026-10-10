import cadquery as cq
import math

R = 50.0           # bend radius of the centerline path
r_start = 15.0     # start radius (30 mm diameter)
r_end = 7.5        # end radius (15 mm diameter)
n = 12             # number of sections along the quarter arc

wires = []
for i in range(n + 1):
    s = i / n
    t = s * math.pi / 2
    center = cq.Vector(R * math.cos(t), R * math.sin(t), 0)
    tangent = cq.Vector(-math.sin(t), math.cos(t), 0)
    r = r_start + (r_end - r_start) * s
    wires.append(cq.Wire.makeCircle(r, center, tangent))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
