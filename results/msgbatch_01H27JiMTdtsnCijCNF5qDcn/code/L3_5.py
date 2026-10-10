import cadquery as cq
import math

# Profile points (XY plane, revolve about Y axis)
n = 24
outer = []
inner = []
for i in range(n + 1):
    t = (math.pi / 2) * i / n
    x = 100 * math.cos(t)
    y = 50 + 50 * math.sin(t)
    nx = math.cos(t) / 100.0
    ny = math.sin(t) / 50.0
    l = math.hypot(nx, ny)
    nx /= l
    ny /= l
    outer.append((x, y))
    inner.append((x - 10 * nx, y - 10 * ny))

# outer goes from (100,50) to (0,100); inner reversed: from (0,90) to (90,50)
outer_pts = outer
inner_pts = inner[::-1]

prof = (
    cq.Workplane("XY")
    .moveTo(90, 0)
    .lineTo(100, 0)
    .lineTo(100, 50)
    .spline(outer_pts[1:], includeCurrent=True)
    .lineTo(0, 90)
    .spline(inner_pts[1:], includeCurrent=True)
    .lineTo(90, 0)
    .close()
)

body = prof.revolve(360, (0, 0, 0), (0, 1, 0))

# Nozzle ring on tangent plane at top vertex (y=100), extruded outward (+Y)
pl = cq.Plane(origin=(0, 100, 0), xDir=(1, 0, 0), normal=(0, 1, 0))
nozzle = (
    cq.Workplane(pl)
    .circle(20)
    .circle(15)
    .extrude(30)
)

result = body.union(nozzle)
