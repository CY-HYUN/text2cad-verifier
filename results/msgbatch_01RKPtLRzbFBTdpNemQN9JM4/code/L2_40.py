import cadquery as cq
import math

R = 15.0
depth = 1.0
L = 60.0
N = 47  # teeth around circumference -> ~2 mm pitch
twist = math.degrees(L / R)  # 45 degree helix: tangential travel = axial travel

pts = []
for i in range(N):
    a0 = 2 * math.pi * i / N
    a1 = 2 * math.pi * (i + 0.5) / N
    pts.append((R * math.cos(a0), R * math.sin(a0)))
    pts.append(((R - depth) * math.cos(a1), (R - depth) * math.sin(a1)))

right = (cq.Workplane("XY").polyline(pts).close()
         .twistExtrude(L, twist))
left = (cq.Workplane("XY").polyline(pts).close()
        .twistExtrude(L, -twist))

result = right.intersect(left)
