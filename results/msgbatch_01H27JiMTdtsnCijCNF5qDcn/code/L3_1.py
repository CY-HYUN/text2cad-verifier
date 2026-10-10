import cadquery as cq
import math

# Parabola: vertex (100,75), focus distance f=50 -> (y-75)^2 = 200*(x-100), truncated at x=200
f = 50.0
vx, vy = 100.0, 75.0
smax = math.sqrt(4 * f * 100.0)  # half-height at x=200

n = 24
pts = []
for i in range(n + 1):
    s = smax * i / n
    pts.append((vx + s * s / (4 * f), vy + s))

profile = (
    cq.Workplane("XY")
    .moveTo(vx, vy)
    .spline(pts[1:], includeCurrent=True)
    .lineTo(200, vy)
    .close()
)

# Revolve 360° about the horizontal axis at Y=75
result = profile.revolve(360, (0, vy, 0), (1, vy, 0))
