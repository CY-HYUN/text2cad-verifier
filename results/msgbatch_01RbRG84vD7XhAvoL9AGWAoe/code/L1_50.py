import cadquery as cq

r = 10.0
L = 50.0

# Vertical cylinder along Z
cyl_z = cq.Workplane("XY").circle(r).extrude(L)

# Horizontal cylinder along X, sharing the end at the origin
cyl_x = cq.Workplane("YZ").circle(r).extrude(L)

result = cyl_z.union(cyl_x)
