import cadquery as cq
import math

# Base
base = cq.Workplane("XY").box(100, 50, 5, centered=False)

A = 2.0
k = 0.2 * math.pi
t = 1.0
h = t / 2.0
N = 200
H = 30.0

def fin(y0):
    up = []
    lo = []
    for i in range(N + 1):
        x = 100.0 * i / N
        y = A * math.sin(k * x)
        dy = A * k * math.cos(k * x)
        n = math.hypot(dy, 1.0)
        nx, ny = -dy / n, 1.0 / n
        up.append((x + nx * h, y0 + y + ny * h))
        lo.append((x - nx * h, y0 + y - ny * h))
    w = (cq.Workplane("XY").workplane(offset=5)
         .moveTo(*lo[0])
         .spline(lo[1:], includeCurrent=True)
         .lineTo(*up[-1])
         .spline(up[::-1][1:], includeCurrent=True)
         .close()
         .extrude(H))
    return w

result = base
for i in range(5):
    result = result.union(fin(5.0 + 10.0 * i))
