import cadquery as cq
import math

R = 40.0
H = 60.0

# 1. Base cylinder
body = cq.Workplane("XY").circle(R).extrude(H)

# Inclined cut: plane through (0,0,60), 30 deg, left high / right low (in YZ)
ang = math.radians(30)
n_up = cq.Vector(0, math.sin(ang), math.cos(ang))  # outward normal of inclined face
cutter = (
    cq.Workplane(cq.Plane(origin=(0, 0, H), xDir=(1, 0, 0), normal=n_up.toTuple()))
    .rect(400, 400)
    .extrude(200)
)
body = body.cut(cutter)

# 3. Parabolic cavity: x^2 = 40 y, opening radius 30 at the inclined surface, depth 22.5
depth = 22.5
pts = []
N = 30
for i in range(N + 1):
    r = 30.0 * i / N
    pts.append((r, r * r / 40.0))
prof = [(0, 0)] + pts[1:] + [(30.0, depth + 15.0), (0, depth + 15.0)]
para = (
    cq.Workplane("XZ")
    .polyline(prof)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
# vertex below surface along the normal, axis aligned with surface normal
para = (
    para.translate((0, 0, -depth))
    .rotate((0, 0, 0), (1, 0, 0), -30)
    .translate((0, 0, H))
)
body = body.cut(para)

# 4. Sine wave groove on cylindrical surface: z = 30 + 5 sin(6t), depth 2
try:
    M = 240
    vpts = []
    for i in range(M):
        t = 2 * math.pi * i / M
        vpts.append(cq.Vector(R * math.sin(t), R * math.cos(t), 30 + 5 * math.sin(6 * t)))
    path_edge = cq.Edge.makeSpline(vpts, periodic=True)
    path = cq.Workplane("XY").add(cq.Wire.assembleEdges([path_edge]))
    tan = cq.Vector(40, 0, 30).normalized()
    prof_wp = cq.Workplane(
        cq.Plane(origin=(0, R, 30), xDir=(0, 1, 0), normal=tan.toTuple())
    ).circle(2.0)
    groove = prof_wp.sweep(path, isFrenet=False)
    body = body.cut(groove)
except Exception:
    pass

result = body
