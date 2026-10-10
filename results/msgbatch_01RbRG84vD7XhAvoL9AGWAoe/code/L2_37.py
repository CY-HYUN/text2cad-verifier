import cadquery as cq

R_sphere = 20.0
cyl_d = 15.0
cyl_len = 30.0
hole_d = 8.0
hole_depth = 10.0

end = R_sphere + cyl_len  # distance from center to cylinder end face

body = cq.Workplane("XY").sphere(R_sphere)

dirs = [
    cq.Vector(1, 0, 0), cq.Vector(-1, 0, 0),
    cq.Vector(0, 1, 0), cq.Vector(0, -1, 0),
    cq.Vector(0, 0, 1), cq.Vector(0, 0, -1),
]

for d in dirs:
    arm = cq.Solid.makeCylinder(cyl_d / 2.0, end, cq.Vector(0, 0, 0), d)
    body = body.union(cq.Workplane("XY").add(arm))

for d in dirs:
    start = d * (end - hole_depth)
    hole = cq.Solid.makeCylinder(hole_d / 2.0, hole_depth + 0.01, start, d)
    body = body.cut(cq.Workplane("XY").add(hole))

result = body
