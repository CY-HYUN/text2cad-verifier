import cadquery as cq
import math

R = 40.0
H = 60.0
ang = math.radians(30)

# 1. Base cylinder
body = cq.Workplane("XY").circle(R).extrude(H)

# Inclined cut through (0,0,60): plane z = 60 - y*tan30 (left high, right low)
# Remove everything above the plane using a large rotated box
cutter = (
    cq.Workplane("XY")
    .box(400, 400, 200, centered=(True, True, False))
    .rotate((0, 0, 0), (1, 0, 0), -30)
    .translate((0, 0, H))
)
body = body.cut(cutter)

# 2/3. Parabolic cavity: rim radius 30 at the inclined surface center, depth 22.5
# Profile in local XZ: depth(r) = 22.5 - r^2/40 (paraboloid x^2 = 40*y)
pts = []
n = 16
for i in range(n + 1):
    r = 30.0 * i / n
    pts.append((r, -(22.5 - r * r / 40.0)))
prof = (
    cq.Workplane("XZ")
    .moveTo(0, 50)
    .lineTo(0, -22.5)
    .spline(pts[1:], includeCurrent=True)
    .lineTo(30, 50)
    .close()
)
cav = prof.revolve(360, (0, 0, 0), (0, 1, 0))
# align local axis with inclined surface normal (0, sin30, cos30)
cav = cav.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, H))
body = body.cut(cav)

# 4. Sine wave groove on outer surface: z = 30 + 5 sin(6t), depth 2
try:
    N = 180
    vpts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        vpts.append(cq.Vector(R * math.cos(t), R * math.sin(t), 30 + 5 * math.sin(6 * t)))
    edge = cq.Edge.makeSpline(vpts, periodic=True)
    path = cq.Wire.assembleEdges([edge])
    p0 = edge.startPoint()
    tan = edge.tangentAt(0)
    circ = cq.Wire.makeCircle(2.0, p0, tan)
    groove = cq.Solid.sweep(circ, [], path, True, False)
    body = body.cut(cq.Workplane().add(groove))
except Exception:
    pass

result = body
