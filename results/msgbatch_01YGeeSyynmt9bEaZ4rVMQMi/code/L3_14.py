import cadquery as cq
import math

# Base plate: 100 x 50 x 5, corner at origin
L, W, T = 100.0, 50.0, 5.0
base = cq.Workplane("XY").box(L, W, T, centered=False)

# Fin parameters
fin_h = 30.0
thk = 1.0
amp = 2.0
k = 0.2 * math.pi
n = 200

def fin_at(y0):
    xs = [L * i / n for i in range(n + 1)]
    top = [(x, y0 + amp * math.sin(k * x) + thk / 2) for x in xs]
    bot = [(x, y0 + amp * math.sin(k * x) - thk / 2) for x in reversed(xs)]
    prof = (
        cq.Workplane("XY", origin=(0, 0, T))
        .spline(top, includeCurrent=False)
        .lineTo(*bot[0])
        .spline(bot[1:], includeCurrent=True)
        .close()
        .extrude(fin_h)
    )
    return prof

result = base
for i in range(5):
    result = result.union(fin_at(5.0 + 10.0 * i))
