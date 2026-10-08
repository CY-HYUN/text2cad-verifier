import cadquery as cq

R_sphere = 20.0
cyl_d = 15.0
cyl_len = 30.0
hole_d = 8.0
hole_depth = 10.0

end = R_sphere + cyl_len  # cylinder end distance from center

result = cq.Workplane("XY").sphere(R_sphere)

dirs = [
    cq.Vector(1, 0, 0), cq.Vector(-1, 0, 0),
    cq.Vector(0, 1, 0), cq.Vector(0, -1, 0),
    cq.Vector(0, 0, 1), cq.Vector(0, 0, -1),
]

for d in dirs:
    arm = cq.Solid.makeCylinder(cyl_d / 2, end, cq.Vector(0, 0, 0), d)
    result = result.union(cq.Workplane("XY").add(arm))

for d in dirs:
    start = d * (end - hole_depth)
    hole = cq.Solid.makeCylinder(hole_d / 2, hole_depth + 1.0, start, d)
    result = result.cut(cq.Workplane("XY").add(hole))
