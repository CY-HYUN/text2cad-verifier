import cadquery as cq
import math

vx, vy = 100.0, 75.0
f = 50.0
depth = 100.0
ymax = math.sqrt(4 * f * depth)

n = 40
pts = []
for i in range(n + 1):
    s = ymax * i / n
    x = vx + s * s / (4 * f)
    pts.append((x, vy + s))

profile = (
    cq.Workplane("XY")
    .moveTo(vx, vy)
    .spline(pts[1:], includeCurrent=True)
    .lineTo(vx + depth, vy)
    .close()
)

result = profile.revolve(360, (vx, vy, 0), (vx + depth, vy, 0))
