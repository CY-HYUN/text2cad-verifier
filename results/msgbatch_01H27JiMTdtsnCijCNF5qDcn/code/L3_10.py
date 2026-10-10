import cadquery as cq
import math

# inner parabola points z = r^2/80, r from 0..80
n = 24
inner = [(80.0 * i / n, (80.0 * i / n) ** 2 / 80.0) for i in range(n, -1, -1)]

# outer surface: normal offset of 5 mm
outer = []
for i in range(n + 1):
    r = 80.0 * i / n
    z = r * r / 80.0
    L = math.sqrt(1 + (r / 40.0) ** 2)
    nx, nz = (r / 40.0) / L, -1.0 / L
    outer.append((r + 5 * nx, z + 5 * nz))

prof = (
    cq.Workplane("XZ")
    .moveTo(0, outer[0][1])
    .spline(outer[1:], includeCurrent=True)
    .lineTo(85, 80)
    .lineTo(95, 80)
    .lineTo(95, 85)
    .lineTo(80, 85)
    .lineTo(80, 80)
    .spline(inner[1:], includeCurrent=True)
    .close()
)
body = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# central light source hole
hole = cq.Workplane("XY").workplane(offset=-10).circle(5).extrude(30)
body = body.cut(hole)

# 4 mounting holes at R=90, one on +Y
pts = [(90 * math.cos(math.radians(90 + 90 * k)), 90 * math.sin(math.radians(90 + 90 * k))) for k in range(4)]
mh = cq.Workplane("XY").workplane(offset=78).pushPoints(pts).circle(2.5).extrude(10)
result = body.cut(mh)
