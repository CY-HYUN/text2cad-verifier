import cadquery as cq
import math

R_out = 10.0
R_in = 8.0
H_main = 80.0
L_branch = 70.0
half_angle = 30.0

a = math.radians(half_angle)
dir1 = cq.Vector(math.sin(a), 0, math.cos(a))
dir2 = cq.Vector(-math.sin(a), 0, math.cos(a))
junction = cq.Vector(0, 0, H_main)

def cyl(r, h, p, d):
    return cq.Workplane("XY").add(cq.Solid.makeCylinder(r, h, p, d))

def sph(r, p):
    return cq.Workplane("XY").sphere(r).translate((p.x, p.y, p.z))

# Outer body
outer = cyl(R_out, H_main, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
outer = outer.union(sph(R_out, junction))
outer = outer.union(cyl(R_out, L_branch, junction, dir1))
outer = outer.union(cyl(R_out, L_branch, junction, dir2))

# Inner cavity (extended slightly through the open ends)
inner = cyl(R_in, H_main + 1, cq.Vector(0, 0, -1), cq.Vector(0, 0, 1))
inner = inner.union(sph(R_in, junction))
inner = inner.union(cyl(R_in, L_branch + 1, junction, dir1))
inner = inner.union(cyl(R_in, L_branch + 1, junction, dir2))

result = outer.cut(inner)
