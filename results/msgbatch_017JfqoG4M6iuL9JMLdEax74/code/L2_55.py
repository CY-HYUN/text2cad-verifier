import cadquery as cq
import math

R_path = 50.0
r_start = 15.0   # 30 mm diameter
r_end = 7.5      # 15 mm diameter
n = 12

wires = []
for i in range(n + 1):
    t = (math.pi / 2) * i / n
    center = cq.Vector(R_path - R_path * math.cos(t), 0, R_path * math.sin(t))
    normal = cq.Vector(math.sin(t), 0, math.cos(t))
    r = r_start + (r_end - r_start) * i / n
    wires.append(cq.Wire.makeCircle(r, center, normal))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
