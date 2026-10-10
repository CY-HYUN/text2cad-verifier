import cadquery as cq
import math

R = 15.0
depth = 1.0
L = 60.0
N = 47  # circumferential pitch ~2 mm
lead = math.pi * 30.0 / math.tan(math.radians(45))  # 45° helix
twist = 360.0 * L / lead

pts = []
step = 2 * math.pi / N
for k in range(N):
    a0 = k * step
    a1 = (k + 0.5) * step
    pts.append((R * math.cos(a0), R * math.sin(a0)))
    pts.append(((R - depth) * math.cos(a1), (R - depth) * math.sin(a1)))

right = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, twist)
left = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, -twist)

result = right.intersect(left)
