import cadquery as cq
import math

# Base cylinder
body = cq.Workplane("XY").circle(40).extrude(60)

# Inclined cut (plane through (0,0,60), normal in YZ plane, tilted 30 deg, highest at -Y)
a = math.radians(30)
n = cq.Vector(0, math.sin(a), math.cos(a))
pl = cq.Plane(origin=(0, 0, 60), xDir=(1, 0, 0), normal=(n.x, n.y, n.z))
cutter = cq.Workplane(pl).rect(300, 300).extrude(100)
body = body.cut(cutter)

# Paraboloid bowl: x^2+y^2 = 40 z, recessed, radius 30 (depth 22.5)
N = 30
pts = [(30.0 * i / N, -(30.0 * i / N) ** 2 / 40.0) for i in range(N + 1)]
prof = cq.Workplane("XZ").moveTo(0, 0)
for p in pts[1:]:
    prof = prof.lineTo(p[0], p[1])
prof = prof.lineTo(30, 1).lineTo(0, 1).close()
bowl = prof.revolve(360, (0, 0, 0), (0, 1, 0))
bowl = bowl.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, 60))
body = body.cut(bowl)

# Sine wave groove around the cylinder at z=30
M = 144
path_pts = []
for i in range(M):
    t = 2 * math.pi * i / M
    path_pts.append(cq.Vector(40 * math.cos(t), 40 * math.sin(t), 30 + 5 * math.sin(6 * t)))
edge = cq.Edge.makeSpline(path_pts, periodic=True)
wire = cq.Wire.assembleEdges([edge])
tan = cq.Vector(0, 40, 30)
cpl = cq.Plane(origin=(40, 0, 30), xDir=(1, 0, 0), normal=(tan.x, tan.y, tan.z))
groove = cq.Workplane(cpl).circle(2).sweep(cq.Workplane("XY").newObject([wire]), isFrenet=True)
body = body.cut(groove)

result = body
