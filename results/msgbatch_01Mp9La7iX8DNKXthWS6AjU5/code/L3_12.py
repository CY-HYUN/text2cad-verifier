import cadquery as cq
import math

# base cylinder
base = cq.Workplane("XY").circle(40).extrude(60)

# inclined cut (plane through (0,0,60), 30 deg to the horizontal, high on the -Y side)
a = math.radians(30)
n = cq.Vector(0, math.sin(a), math.cos(a))
pl = cq.Plane(origin=(0, 0, 60), xDir=(1, 0, 0), normal=(n.x, n.y, n.z))
cutter = cq.Workplane(pl).rect(300, 300).extrude(150)
body = base.cut(cutter)

# parabolic cavity: x^2 = 40*y, vertex at the centre of the inclined face, axis into the solid
pts = []
N = 20
for i in range(N + 1):
    r = 30.0 * i / N
    pts.append((r, r * r / 40.0))
prof = (cq.Workplane("XZ")
        .moveTo(0, 0)
        .spline(pts[1:], includeCurrent=True)
        .lineTo(0, 22.5)
        .close())
cav = prof.revolve(360, (0, 0, 0), (0, 1, 0))
# local Z (depth) -> -n : rotate 150 deg about X, then move to the face centre
cav = cav.rotate((0, 0, 0), (1, 0, 0), 150).translate((0, 0, 60))
body = body.cut(cav)

# sine wave groove wrapped on the cylindrical surface, depth ~2 mm
M = 240
path_pts = []
for i in range(M):
    t = 2 * math.pi * i / M
    path_pts.append(cq.Vector(40 * math.sin(t), 40 * math.cos(t), 30 + 5 * math.sin(6 * t)))
path = cq.Workplane("XY").newObject([cq.Wire.assembleEdges(
    [cq.Edge.makeSpline(path_pts + [path_pts[0]], periodic=True)])])

start = path_pts[0]
tan = cq.Vector(40, 0, 30)
prof_pl = cq.Plane(origin=(start.x, start.y, start.z), xDir=(0, 1, 0), normal=(tan.x, tan.y, tan.z))
groove = cq.Workplane(prof_pl).circle(1.0).sweep(path, isFrenet=True)
body = body.cut(groove)

result = body
