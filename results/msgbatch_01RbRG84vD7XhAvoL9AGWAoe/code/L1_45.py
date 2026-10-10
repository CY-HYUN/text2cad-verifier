import cadquery as cq

R_out = 50.0
R_in = 40.0

outer = cq.Workplane("XY").sphere(R_out)
inner = cq.Workplane("XY").sphere(R_in)
shell = outer.cut(inner)

# Keep upper half (flat cut plane at z=0 facing downward)
box = cq.Workplane("XY").box(2 * R_out + 10, 2 * R_out + 10, R_out + 10, centered=(True, True, False))
result = shell.intersect(box)
