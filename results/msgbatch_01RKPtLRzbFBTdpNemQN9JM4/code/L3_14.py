import cadquery as cq
import math

base = cq.Workplane("XY").box(100, 50, 5, centered=(False, True, False))

N = 100
def f(x):
    return 2 * math.sin(0.2 * math.pi * x)

result = base
for y0 in [-20, -10, 0, 10, 20]:
    upper = [(100.0 * i / N, y0 + f(100.0 * i / N) + 0.5) for i in range(N + 1)]
    lower = [(100.0 * i / N, y0 + f(100.0 * i / N) - 0.5) for i in range(N, -1, -1)]
    pts = upper + lower
    fin = (cq.Workplane("XY").workplane(offset=5)
           .polyline(pts).close().extrude(30))
    result = result.union(fin)
