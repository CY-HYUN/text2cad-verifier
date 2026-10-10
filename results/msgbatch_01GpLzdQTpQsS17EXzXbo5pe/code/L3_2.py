import math
import cadquery as cq

# Base plate 100 x 50 x 3
plate = cq.Workplane("XY").box(100, 50, 3, centered=False)

# Sine curve sketched on the plate top (z = 3), centred on y = 25
n = 200
yc = 25.0
A = 5.0
d = 1.0

pts1 = []
pts2 = []
for i in range(n + 1):
    t = 100.0 * i / n
    y = yc + A * math.sin(2 * math.pi * t / 20.0)
    pts1.append((t, y))
    pts2.append((t, y + d))  # unidirectional offset of the curve

wp = (
    cq.Workplane("XY").workplane(offset=3)
    .moveTo(*pts1[0])
    .spline(pts1[1:], includeCurrent=True)
    .lineTo(*pts2[-1])
    .spline(pts2[::-1][1:], includeCurrent=True)
    .close()
)
wall = wp.extrude(50.0)

result = plate.union(wall)
