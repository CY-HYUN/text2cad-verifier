import cadquery as cq
import math

# Base plate: 100 x 50 x 5, corner at origin
base = cq.Workplane("XY").box(100, 50, 5, centered=False)

n = 200
t = 1.0   # wall thickness
H = 30.0  # fin height

def fin(y0):
    top = [(100.0 * i / n,
            y0 + 2 * math.sin(0.2 * math.pi * 100.0 * i / n) + t / 2)
           for i in range(n + 1)]
    bot = [(100.0 * i / n,
            y0 + 2 * math.sin(0.2 * math.pi * 100.0 * i / n) - t / 2)
           for i in range(n, -1, -1)]
    pts = top + bot
    return (cq.Workplane("XY").workplane(offset=5)
            .polyline(pts).close()
            .extrude(H))

result = base
for k in range(5):
    result = result.union(fin(5.0 + 10.0 * k))
