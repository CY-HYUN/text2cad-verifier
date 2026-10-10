import cadquery as cq
import math

# Cylinder sleeve (OD 120, bore 90, height 100)
sleeve = cq.Workplane("XY").circle(60).circle(45).extrude(100)

# 15 fins, 2 mm thick, OD 160, pitch 7 mm (first at z=0, last at z=98)
body = sleeve
for i in range(15):
    fin = (cq.Workplane("XY").workplane(offset=7 * i)
           .circle(80).circle(59).extrude(2))
    body = body.union(fin)

# Hemispherical cover, radius 60, on top surface
sphere = cq.Workplane("XY").sphere(60).translate((0, 0, 100))
keep = cq.Workplane("XY").workplane(offset=100).circle(70).extrude(70)
dome = sphere.intersect(keep)
body = body.union(dome)

# Intake / exhaust tubes at asymmetric inclined angles
def tube(angle_deg, side):
    a = math.radians(angle_deg)
    d = cq.Vector(side * math.sin(a), 0, math.cos(a))
    base = cq.Vector(0, 0, 100)
    start = base + d * 20
    outer = cq.Solid.makeCylinder(15, 70, start, d)
    inner = cq.Solid.makeCylinder(10, 95, base, d)
    return cq.Workplane("XY").add(outer), cq.Workplane("XY").add(inner)

o1, i1 = tube(35, 1)
o2, i2 = tube(50, -1)
body = body.union(o1).union(o2)
body = body.cut(i1).cut(i2)

# Spark plug hole, dia 14, vertical from apex down into the chamber
plug = cq.Workplane("XY").workplane(offset=100).circle(7).extrude(61)
body = body.cut(plug)

# Four bolt holes at quadrant points through the sleeve/fin height
r = 70
for k in range(4):
    ang = math.radians(45 + 90 * k)
    hole = (cq.Workplane("XY").workplane(offset=-1)
            .center(r * math.cos(ang), r * math.sin(ang))
            .circle(5).extrude(102))
    body = body.cut(hole)

result = body
