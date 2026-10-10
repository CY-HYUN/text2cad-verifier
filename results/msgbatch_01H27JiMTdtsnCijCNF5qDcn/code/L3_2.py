import cadquery as cq
import math

# Base plate: 100 x 50 x 3, x from 0..100, y from -25..25
plate = cq.Workplane("XY").box(100, 50, 3, centered=(False, True, False))

# Sine curve and normal-offset curve (1 mm)
d = 1.0
N = 200
p1 = []
p2 = []
for i in range(N + 1):
    t = 100.0 * i / N
    y = 5 * math.sin(2 * math.pi * t / 20)
    dy = 5 * (2 * math.pi / 20) * math.cos(2 * math.pi * t / 20)
    L = math.sqrt(1 + dy * dy)
    p1.append((t, y))
    p2.append((t - d * dy / L, y + d / L))

wp = cq.Workplane("XY").workplane(offset=3)
profile = (
    wp.moveTo(*p1[0])
    .spline(p1[1:], includeCurrent=True)
    .lineTo(*p2[-1])
    .spline(list(reversed(p2))[1:], includeCurrent=True)
    .close()
)
band = profile.extrude(50.0)

result = plate.union(band)
