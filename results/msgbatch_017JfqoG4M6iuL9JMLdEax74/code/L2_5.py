import cadquery as cq
import math

R_out = 10.0   # 20 mm outer diameter
R_in = 8.0     # 2 mm wall
L_main = 40.0
L_branch = 40.0
half_angle = math.radians(30)  # 60 deg between branches

def cyl(r, h, p, d):
    return cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d))

dirs = [(math.sin(half_angle), 0, math.cos(half_angle)),
        (-math.sin(half_angle), 0, math.cos(half_angle))]

# Outer solid
outer = cq.Workplane().add(cyl(R_out, L_main, (0, 0, -L_main), (0, 0, 1)))
for d in dirs:
    outer = outer.union(cq.Workplane().add(cyl(R_out, L_branch, (0, 0, 0), d)))
outer = outer.union(cq.Workplane().add(cq.Solid.makeSphere(R_out, angleDegrees1=-90, angleDegrees2=90)))

# Inner cavity (extended past ends for clean openings)
ext = 1.0
inner = cq.Workplane().add(cyl(R_in, L_main + ext, (0, 0, -L_main - ext), (0, 0, 1)))
for d in dirs:
    inner = inner.union(cq.Workplane().add(cyl(R_in, L_branch + ext, (0, 0, 0), d)))
inner = inner.union(cq.Workplane().add(cq.Solid.makeSphere(R_in, angleDegrees1=-90, angleDegrees2=90)))

result = outer.cut(inner)
