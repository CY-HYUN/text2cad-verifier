import cadquery as cq
import math

# Base plate 100 x 50 x 3
L, W, T = 100.0, 50.0, 3.0
base = cq.Workplane("XY").box(L, W, T, centered=False)

# Sine band profile: y(t) = 5*sin(2*pi*t/20), t in [0,100], offset 1.0 mm
A, P, th = 5.0, 20.0, 1.0
n = 201
lower = [(L * i / (n - 1), T + A * math.sin(2 * math.pi * (L * i / (n - 1)) / P)) for i in range(n)]
upper = [(x, z + th) for (x, z) in lower]

# Closed profile on XZ plane (wave in X, amplitude in Z)
wp = cq.Workplane("XZ")
prof = (
    wp.moveTo(*lower[0])
    .spline(lower[1:], includeCurrent=True)
    .lineTo(*upper[-1])
    .spline(list(reversed(upper))[1:], includeCurrent=True)
    .close()
)
# XZ normal is -Y, so extrude negative to go +Y across the 50 mm width
fin = prof.extrude(-W)

result = base.union(fin)
