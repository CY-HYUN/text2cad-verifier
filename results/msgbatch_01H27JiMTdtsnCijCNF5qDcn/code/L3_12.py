import cadquery as cq
import math

# 1. Base cylinder (D80 x 60)
body = cq.Workplane("XY").circle(40).extrude(60)

# Inclined cut: plane through (0,0,60), 30 deg to horizontal in the YZ plane, high on the left (-Y)
t30 = math.tan(math.radians(30))
cutter = (
    cq.Workplane("XY").box(300, 300, 100, centered=(True, True, False))
    .translate((0, 0, 0))
)
# box sits above the plane z = 60 - tan30*y: rotate about X, then move to (0,0,60)
cutter = cutter.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, 60))
body = body.cut(cutter)

# 3. Parabolic cavity: x^2 = 40 d, from the surface down to r=30, depth 22.5
pts = []
n = 20
for i in range(n, -1, -1):
    r = 30.0 * i / n
    pts.append((r, -(r * r) / 40.0))
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(30, 0)
    .lineTo(30, -22.5)
    .spline(pts[1:], includeCurrent=True)
    .close()
)
cavity = profile.revolve(360, (0, 0, 0), (0, 1, 0))
# align local Z with the inward-opposite surface normal (0, 0.5, 0.866), place at the centre of the inclined face
cavity = cavity.rotate((0, 0, 0), (1, 0, 0), -30).translate((0, 0, 60))
body = body.cut(cavity)

# 4. Sine wave groove wrapped on the cylindrical surface, depth 2
N = 144
path_pts = []
for i in range(N):
    t = 2 * math.pi * i / N
    path_pts.append((40 * math.cos(t), 40 * math.sin(t), 30 + 5 * math.sin(6 * t)))
path = cq.Workplane("XY").spline(path_pts, periodic=True)

tan = cq.Vector(0, 40, 30).normalized()
plane = cq.Plane(origin=(40, 0, 30), xDir=(1, 0, 0), normal=(tan.x, tan.y, tan.z))
groove = cq.Workplane(plane).circle(2.0).sweep(path)
body = body.cut(groove)

result = body
