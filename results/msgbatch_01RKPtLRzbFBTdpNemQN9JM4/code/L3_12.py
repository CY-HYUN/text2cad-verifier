import cadquery as cq
import math

R = 40.0
H_ext = 90.0
tilt = math.radians(30)

# Base cylinder (extended; the top is trimmed by the inclined plane)
body = cq.Workplane("XY").circle(R).extrude(H_ext)

# Inclined cutting plane through (0,0,60), normal (0, sin30, cos30); highest toward -Y
n = cq.Vector(0, math.sin(tilt), math.cos(tilt))
cut_box = (
    cq.Workplane("XY")
    .rect(300, 300)
    .extrude(150)
    .translate((0, 0, 0))
)
# rotate box so its bottom face lies on the inclined plane
cut_box = cut_box.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, 60))
body = body.cut(cut_box)

# Paraboloid recess: x^2+y^2 = 40 z (local), opening diameter 60
pts = [(i * 30.0 / 40, -(i * 30.0 / 40) ** 2 / 40.0) for i in range(41)]
prof = cq.Workplane("XZ").moveTo(0, 0)
for p in pts[1:]:
    prof = prof.lineTo(*p)
prof = prof.lineTo(30, 10).lineTo(0, 10).close()
para = prof.revolve(360, (0, 0, 0), (0, 1, 0))
para = para.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, 60))
body = body.cut(para)

# Sine wave groove around the cylinder at z=30, 6 cycles, amplitude 5
N = 144
vecs = []
for i in range(N):
    t = 2 * math.pi * i / N
    vecs.append(cq.Vector(R * math.cos(t), R * math.sin(t), 30 + 5 * math.sin(6 * t)))
edge = cq.Edge.makeSpline(vecs, periodic=True)
path = cq.Wire.assembleEdges([edge])

tang = cq.Vector(0, 40.0, 30.0).normalized()
pl = cq.Plane(origin=(R, 0, 30), xDir=(1, 0, 0), normal=(tang.x, tang.y, tang.z))
groove = cq.Workplane(pl).circle(2.0).sweep(cq.Workplane("XY").add(path), isFrenet=True)

result = body.cut(groove)
