import cadquery as cq
import math

# Cylinder liner
liner = cq.Workplane("XY").circle(60).extrude(100)

# 15 annular fins (2 mm thick, OD 160), pitch 7 mm
body = liner
for i in range(15):
    fin = (cq.Workplane("XY").workplane(offset=i * 7)
           .circle(80).circle(58).extrude(2))
    body = body.union(fin)

# Hemispherical cover
sph = cq.Workplane("XY").sphere(60).translate((0, 0, 100))
box = cq.Workplane("XY").workplane(offset=100).rect(200, 200).extrude(100)
dome = sph.intersect(box)
body = body.union(dome)

# Intake / exhaust pipes (asymmetric)
def pipe(angle_deg, side, r, start, length):
    a = math.radians(angle_deg)
    d = cq.Vector(side * math.sin(a), 0, math.cos(a))
    p = cq.Vector(0, 0, 100) + d * start
    return cq.Workplane("XY").add(cq.Solid.makeCylinder(r, length, p, d))

intake_o = pipe(60, 1, 13, 30, 65)
exhaust_o = pipe(50, -1, 15, 30, 55)
body = body.union(intake_o).union(exhaust_o)

# Cylinder bore and combustion cavity
bore = cq.Workplane("XY").circle(40).extrude(100)
cavity = cq.Workplane("XY").sphere(40).translate((0, 0, 100))
body = body.cut(bore).cut(cavity)

# Port bores
intake_i = pipe(60, 1, 9, 20, 80)
exhaust_i = pipe(50, -1, 11, 20, 70)
body = body.cut(intake_i).cut(exhaust_i)

# Spark plug hole, 14 mm dia at top center
spark = cq.Workplane("XY").workplane(offset=120).circle(7).extrude(50)
body = body.cut(spark)

# Four bolt holes through full height at quadrant points
pts = [(70 * math.cos(math.radians(a)), 70 * math.sin(math.radians(a)))
       for a in (45, 135, 225, 315)]
bolts = (cq.Workplane("XY").workplane(offset=-1)
         .pushPoints(pts).circle(5).extrude(102))
body = body.cut(bolts)

result = body
