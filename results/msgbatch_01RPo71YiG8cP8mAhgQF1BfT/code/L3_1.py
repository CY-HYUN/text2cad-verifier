import cadquery as cq
import math

# Paraboloid reflector: (y-75)^2 + z^2 = 200 (x - 100), x in [100, 200]
# Built as a thin solid shell (2 mm thick behind the reflective surface)
vx, vy = 100.0, 75.0
f = 50.0
depth = 100.0
t = 2.0                       # shell thickness (backside offset along -X)
R = math.sqrt(4 * f * depth)  # rim radius ~141.42

N = 40
inner = []
outer = []
for i in range(N + 1):
    r = R * i / N
    dx = r * r / (4 * f)
    inner.append((vx + dx, vy + r))
    outer.append((vx - t + dx, vy + r))

tan_vertex = (0.0, 1.0)
tan_rim = (R / (2 * f), 1.0)

outer_rev = list(reversed(outer))

profile = (
    cq.Workplane("XY")
    .moveTo(vx, vy)
    .spline(inner[1:], tangents=[tan_vertex, tan_rim], includeCurrent=True)
    .lineTo(outer_rev[0][0], outer_rev[0][1])
    .spline(outer_rev[1:], tangents=[(-tan_rim[0], -tan_rim[1]), (0.0, -1.0)],
            includeCurrent=True)
    .close()
)

result = profile.revolve(360, (vx, vy, 0), (vx + depth, vy, 0))
