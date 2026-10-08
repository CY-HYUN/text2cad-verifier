import cadquery as cq

R_sphere = 20.0
r_cyl = 7.5
L = 30.0
r_hole = 4.0
depth = 10.0

result = cq.Workplane("XY").sphere(R_sphere)

dirs = [
    cq.Vector(1, 0, 0), cq.Vector(-1, 0, 0),
    cq.Vector(0, 1, 0), cq.Vector(0, -1, 0),
    cq.Vector(0, 0, 1), cq.Vector(0, 0, -1),
]

for d in dirs:
    cyl = cq.Solid.makeCylinder(r_cyl, L, cq.Vector(0, 0, 0), d)
    result = result.union(cq.Workplane("XY").add(cyl))

for d in dirs:
    start = d * (L - depth)
    hole = cq.Solid.makeCylinder(r_hole, depth + 0.01, start, d)
    result = result.cut(cq.Workplane("XY").add(hole))

result = result.clean()
