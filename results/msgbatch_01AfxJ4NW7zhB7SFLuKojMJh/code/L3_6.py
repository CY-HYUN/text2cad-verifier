import cadquery as cq
import math

R = 20.0
L = 100.0
z0 = 50.0
A = 30.0

body = cq.Workplane("XY").circle(R).extrude(L)

# groove center path (ball centre at r = 19, i.e. 1 mm below surface)
rc = R - 1.0
N = 90
pts = []
for i in range(N):
    p = 2 * math.pi * i / N
    pts.append(cq.Vector(rc * math.cos(p), rc * math.sin(p), z0 + A * math.sin(p)))
edge = cq.Edge.makeSpline(pts, periodic=True)
path = cq.Wire.assembleEdges([edge])

# profile plane at phi = 0, perpendicular to the path tangent
tx = cq.Vector(0, rc, A).normalized()
w = cq.Vector(0, -A, rc).normalized()
plane = cq.Plane(origin=(rc, 0, z0), xDir=(w.x, w.y, w.z), normal=(tx.x, tx.y, tx.z))

round_part = cq.Workplane(plane).circle(3.0).sweep(path, isFrenet=True)
slot_part = (
    cq.Workplane(plane).center(0, 1.0).rect(6.0, 2.0).sweep(path, isFrenet=True)
)

groove = round_part.union(slot_part)
result = body.cut(groove)
