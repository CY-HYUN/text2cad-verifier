import cadquery as cq

R_out = 20.0
t = 2.0
R_in = R_out - t
half_len = 50.0

# Outer cross: two cylinders along X and Y, unioned
cyl_x = cq.Workplane("YZ").circle(R_out).extrude(half_len, both=True)
cyl_y = cq.Workplane("XZ").circle(R_out).extrude(half_len, both=True)
outer = cyl_x.union(cyl_y)

# Inner void (equivalent to shell of 2mm with the four end faces removed)
in_x = cq.Workplane("YZ").circle(R_in).extrude(half_len, both=True)
in_y = cq.Workplane("XZ").circle(R_in).extrude(half_len, both=True)
inner = in_x.union(in_y)

result = outer.cut(inner)
