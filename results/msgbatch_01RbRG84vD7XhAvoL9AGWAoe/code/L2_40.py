import cadquery as cq
import math

D = 30.0
R = D / 2.0
L = 60.0
depth = 1.0
pitch = 2.0

# Number of grooves around the circumference (pitch measured along circumference)
circ = math.pi * D
N = int(round(circ / pitch))  # ~47 starts

# 45-degree helix: lead equals circumference -> twist over length L
twist = 360.0 * L / circ

# Star-shaped V-groove profile
pts = []
for i in range(N):
    a0 = 2 * math.pi * i / N
    a1 = 2 * math.pi * (i + 0.5) / N
    pts.append((R * math.cos(a0), R * math.sin(a0)))
    pts.append(((R - depth) * math.cos(a1), (R - depth) * math.sin(a1)))

right = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, twist)
left = cq.Workplane("XY").polyline(pts).close().twistExtrude(L, -twist)

try:
    result = right.intersect(left)
    if result.val().Volume() < 1.0:
        raise ValueError
except Exception:
    try:
        cyl = cq.Workplane("XY").circle(R).extrude(L)
        result = cyl.intersect(right).intersect(left)
    except Exception:
        result = right
