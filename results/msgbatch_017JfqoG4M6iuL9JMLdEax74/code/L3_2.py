import cadquery as cq
import math

L, W, T = 100.0, 50.0, 3.0
A, lam, off = 5.0, 20.0, 5.0
t = 1.0
N = 600

# Base: top surface at Y=0
base = cq.Workplane("XY").box(L, T, W, centered=False).translate((0, -T, 0))

# Fin profile: offset sine centerline by +/- t/2 along normal
upper, lower = [], []
for i in range(N + 1):
    x = L * i / N
    y = A * math.sin(2 * math.pi * x / lam) + off
    dy = A * (2 * math.pi / lam) * math.cos(2 * math.pi * x / lam)
    n = math.sqrt(1 + dy * dy)
    nx, ny = -dy / n, 1 / n
    upper.append((x + 0.5 * t * nx, y + 0.5 * t * ny))
    lower.append((x - 0.5 * t * nx, y - 0.5 * t * ny))

pts = upper + lower[::-1]
fin = cq.Workplane("XY").polyline(pts).close().extrude(W)

# Trim fin to base length
clip = cq.Workplane("XY").box(L, 20, W, centered=False).translate((0, -T, 0))
fin = fin.intersect(clip)

result = base.union(fin)
