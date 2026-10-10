import cadquery as cq
import math

R = 15.0
depth = 1.0
L = 60.0
N = 48  # grooves per direction (~2 mm pitch around the circumference)

# 45-degree helix: axial travel equals arc length travel -> twist angle = L / R radians
twist = math.degrees(L / R)

pts = []
for i in range(2 * N):
    a = math.pi * i / N
    r = R if i % 2 == 0 else R - depth
    pts.append((r * math.cos(a), r * math.sin(a)))

right = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, twist)
left = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, -twist)

result = right.intersect(left)
