import cadquery as cq
import math

R_path = 50.0
r_start = 15.0   # 30 mm diameter
r_end = 7.5      # 15 mm diameter

# Path: 90-degree arc in the front (XZ) plane, centred at the origin.
# P(t) = (R cos t, 0, R sin t), tangent T(t) = (-sin t, 0, cos t).
n = 13
wires = []
for i in range(n):
    f = i / (n - 1)
    t = f * math.pi / 2
    center = cq.Vector(R_path * math.cos(t), 0, R_path * math.sin(t))
    normal = cq.Vector(-math.sin(t), 0, math.cos(t))
    # Linear diameter change along the centreline.
    r = r_start + (r_end - r_start) * f
    wires.append(cq.Wire.makeCircle(r, center, normal))

solid = cq.Solid.makeLoft(wires, False)
result = cq.Workplane("XY").add(solid)
