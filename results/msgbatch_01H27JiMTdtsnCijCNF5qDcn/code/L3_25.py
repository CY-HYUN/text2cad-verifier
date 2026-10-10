import cadquery as cq
import math

# Sleeve body: OD 120, bore 90, height 100
body = (cq.Workplane("XY").circle(60).circle(45).extrude(100))

# 15 fins, OD 160, 2 mm thick, equal pitch (7 mm) from z=0 to z=100
fins = None
for i in range(15):
    f = (cq.Workplane("XY").workplane(offset=7 * i)
         .circle(80).circle(60).extrude(2))
    fins = f if fins is None else fins.union(f)
body = body.union(fins)

# Hemispherical cover (shell), radius 60, inner cavity radius 45
sph = cq.Workplane("XY").sphere(60)
cav = cq.Workplane("XY").sphere(45)
lower = cq.Workplane("XY").box(400, 400, 400, centered=(True, True, False)).translate((0, 0, -400))
dome = sph.cut(lower).cut(cav).translate((0, 0, 100))
head = body.union(dome)

# Inclined intake / exhaust tubes at asymmetric angles
def tube(angle, od, length_start=50, length=55):
    t = (cq.Workplane("XY").workplane(offset=length_start)
         .circle(od / 2).extrude(length))
    return t.rotate((0, 0, 0), (0, 1, 0), angle).translate((0, 0, 100))

def bore(angle, d):
    b = cq.Workplane("XY").circle(d / 2).extrude(106)
    return b.rotate((0, 0, 0), (0, 1, 0), angle).translate((0, 0, 100))

a1, a2 = 35, -50
head = head.union(tube(a1, 24)).union(tube(a2, 24))
head = head.cut(bore(a1, 16)).cut(bore(a2, 16))

# Spark plug hole, dia 14, from apex downward
plug = cq.Workplane("XY").workplane(offset=100).circle(7).extrude(70)
head = head.cut(plug)

# Four bolt holes through total height at quadrant points
r = 70
for k in range(4):
    ang = math.radians(45 + 90 * k)
    h = (cq.Workplane("XY").workplane(offset=-1)
         .center(r * math.cos(ang), r * math.sin(ang))
         .circle(5).extrude(165))
    head = head.cut(h)

result = head
