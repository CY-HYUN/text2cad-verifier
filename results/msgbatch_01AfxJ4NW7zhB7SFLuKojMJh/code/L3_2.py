import cadquery as cq
import math

L = 100.0
W = 50.0
T = 3.0
A = 5.0
wl = 20.0
t = 1.0

# Base: top surface at Y=0
base = cq.Workplane("XY").box(L, T, W, centered=False).translate((0, -T, 0))

# Sinusoidal fin profile (thickness offset along the normal)
N = 250
upper = []
lower = []
for i in range(N + 1):
    x = L * i / N
    y = A * math.sin(2 * math.pi * x / wl) + A
    dy = A * (2 * math.pi / wl) * math.cos(2 * math.pi * x / wl)
    n = math.hypot(dy, 1.0)
    nx, ny = -dy / n, 1.0 / n
    upper.append((x + 0.5 * t * nx, y + 0.5 * t * ny))
    lower.append((x - 0.5 * t * nx, y - 0.5 * t * ny))

profile = (
    cq.Workplane("XY")
    .moveTo(*upper[0])
    .spline(upper[1:], includeCurrent=True)
    .lineTo(*lower[-1])
    .spline(lower[::-1][1:], includeCurrent=True)
    .close()
)
fin = profile.extrude(W)

result = base.union(fin)
