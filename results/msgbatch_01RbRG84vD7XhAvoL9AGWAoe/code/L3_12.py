import cadquery as cq
import math

R = 40.0
H = 60.0
tilt = math.radians(30)
f = 10.0
open_r = 30.0
depth = open_r**2 / (4 * f)  # 22.5

# Base cylinder, built tall then trimmed by the inclined plane
base = cq.Workplane("XY").circle(R).extrude(H + 60)

# Inclined plane through (0,0,H); z = H - y*tan(30) so the high side is at -Y
n = cq.Vector(0, math.sin(tilt), math.cos(tilt))
cutter = (
    cq.Workplane(cq.Plane(origin=(0, 0, H), xDir=(1, 0, 0), normal=n.toTuple()))
    .rect(400, 400)
    .extrude(200)
)
body = base.cut(cutter)

# Paraboloid bowl (x^2 + y^2 = 40 z in local coordinates)
pts = [(r, r * r / (4 * f)) for r in [open_r * i / 30.0 for i in range(1, 31)]]
prof = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline([(0, 0)] + pts, includeCurrent=False)
    .lineTo(open_r, depth + 30)
    .lineTo(0, depth + 30)
    .close()
)
bowl = prof.revolve(360, (0, 0, 0), (0, 1, 0))
bowl = bowl.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, H))
body = body.cut(bowl)

# Sine-wave groove around the side wall
N = 180
amp = 5.0
cycles = 6
zc = 30.0
vpts = []
for i in range(N):
    t = 2 * math.pi * i / N
    vpts.append(cq.Vector(R * math.cos(t), R * math.sin(t), zc + amp * math.sin(cycles * t)))
edge = cq.Edge.makeSpline(vpts, periodic=True)
path = cq.Wire.assembleEdges([edge])

start = cq.Vector(R, 0, zc)
tangent = cq.Vector(0, R, amp * cycles)
groove = (
    cq.Workplane(cq.Plane(origin=start.toTuple(), xDir=(1, 0, 0), normal=tangent.normalized().toTuple()))
    .circle(2.0)
    .sweep(cq.Workplane(obj=path), isFrenet=True)
)
body = body.cut(groove)

result = body
