import cadquery as cq
import math

R_out = 10.0   # 20 mm outer diameter
R_in = 8.0     # 2 mm wall
L_main = 40.0
L_branch = 40.0
half_angle = math.radians(30)  # 60 deg between branches

dirs = [cq.Vector(math.sin(half_angle), 0, math.cos(half_angle)),
        cq.Vector(-math.sin(half_angle), 0, math.cos(half_angle))]

# Outer body
outer = cq.Solid.makeCylinder(R_out, L_main, cq.Vector(0, 0, -L_main), cq.Vector(0, 0, 1))
for d in dirs:
    outer = outer.fuse(cq.Solid.makeCylinder(R_out, L_branch, cq.Vector(0, 0, 0), d))
outer = outer.fuse(cq.Solid.makeSphere(R_out, cq.Vector(0, 0, 0)))

# Inner cavity (connected through junction sphere)
inner = cq.Solid.makeCylinder(R_in, L_main + 1, cq.Vector(0, 0, -L_main - 1), cq.Vector(0, 0, 1))
for d in dirs:
    inner = inner.fuse(cq.Solid.makeCylinder(R_in, L_branch + 1, cq.Vector(0, 0, 0), d))
inner = inner.fuse(cq.Solid.makeSphere(R_in, cq.Vector(0, 0, 0)))

body = outer.cut(inner)
result = cq.Workplane("XY").add(body).clean()
