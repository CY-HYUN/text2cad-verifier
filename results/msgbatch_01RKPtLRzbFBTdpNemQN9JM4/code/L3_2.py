import cadquery as cq
import math

L = 100.0
W = 50.0
T_base = 3.0
amp = 5.0
wl = 20.0
t = 1.0

# Base: X 0..100, Y -3..0, Z 0..50
base = cq.Workplane("XY").box(L, T_base, W, centered=False).translate((0, -T_base, 0))

# Fin centerline and normal-offset curves
N = 400
upper = []
lower = []
for i in range(N + 1):
    x = L * i / N
    k = 2 * math.pi / wl
    y = amp * math.sin(k * x) + amp
    dy = amp * k * math.cos(k * x)
    n = math.sqrt(1 + dy * dy)
    nx, ny = -dy / n, 1 / n
    upper.append((x + 0.5 * t * nx, y + 0.5 * t * ny))
    lower.append((x - 0.5 * t * nx, y - 0.5 * t * ny))

prof = (
    cq.Workplane("XY")
    .moveTo(*upper[0])
    .spline(upper[1:], includeCurrent=True)
    .lineTo(*lower[-1])
    .spline(lower[::-1][1:], includeCurrent=True)
    .close()
)
fin = prof.extrude(W)

result = base.union(fin)
