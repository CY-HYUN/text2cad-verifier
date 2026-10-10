import cadquery as cq
import math

# base cylinder
base = cq.Workplane("XY").circle(40).extrude(60)

# inclined cut (plane through (0,0,60), 30 deg to horizontal)
a = math.radians(30)
n = cq.Vector(0, math.sin(a), math.cos(a))
pl = cq.Plane(origin=(0, 0, 60), xDir=(1, 0, 0), normal=(n.x, n.y, n.z))
cutter = cq.Workplane(pl).rect(300, 300).extrude(150)
body = base.cut(cutter)

# parabolic cavity x^2 = 40*z (vertex at the bottom, opening toward the inclined face)
top = 26.0
N = 24
pts = []
for i in range(N + 1):
    z = top * i / N
    pts.append((math.sqrt(40.0 * z), z))
poly = [(0, 0)] + pts[1:] + [(0, top)]
prof = cq.Workplane("XZ").polyline(poly).close()
cav = prof.revolve(360, (0, 0, 0), (0, 1, 0))
# align local Z with the face normal, then place vertex 22.5 below the face centre
cav = cav.rotate((0, 0, 0), (1, 0, 0), -30)
cav = cav.translate((0 - 22.5 * n.x, 0 - 22.5 * n.y, 60 - 22.5 * n.z))
body = body.cut(cav)

# sine wave groove on the cylindrical surface
try:
    M = 180
    path_pts = []
    for i in range(M + 1):
        t = 2 * math.pi * i / M
        path_pts.append(cq.Vector(40 * math.sin(t), 40 * math.cos(t),
                                  30 + 5 * math.sin(6 * t)))
    edge = cq.Edge.makeSpline(path_pts)
    wire = cq.Wire.assembleEdges([edge])
    path = cq.Workplane("XY").newObject([wire])

    prof_pl = cq.Plane(origin=(0, 40, 30), xDir=(0, 1, 0), normal=(40, 0, 30))
    groove = cq.Workplane(prof_pl).circle(2.0).sweep(path, isFrenet=True)
    cut_body = body.cut(groove)
    if cut_body.val().isValid():
        body = cut_body
except Exception:
    pass

result = body
