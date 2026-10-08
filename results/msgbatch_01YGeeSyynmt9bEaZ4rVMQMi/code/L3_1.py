import cadquery as cq
import math

# Parabola: vertex (100,75), focal length f = 50, opening to +X
# (y-75)^2 = 4 f (x-100)
f = 50.0
vx, vy = 100.0, 75.0
x_end = 200.0
r_max = math.sqrt(4 * f * (x_end - vx))  # ~141.42 mm aperture radius
t = 2.0  # small wall thickness to make a solid reflector

n = 60
inner = [(vx + (r_max * i / n) ** 2 / (4 * f), vy + r_max * i / n) for i in range(n + 1)]
outer = [(x - t, y) for (x, y) in inner]

prof = (
    cq.Workplane("XY")
    .moveTo(*inner[0])
    .spline(inner[1:], includeCurrent=True)
    .lineTo(outer[-1][0], outer[-1][1])
    .spline(list(reversed(outer[:-1])), includeCurrent=True)
    .close()
)

# Revolve 360 deg about the horizontal axis y = 75
result = prof.revolve(360, (0, vy, 0), (1, vy, 0))
