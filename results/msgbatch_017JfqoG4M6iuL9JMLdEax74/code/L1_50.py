import cadquery as cq

d = 20.0
r = d / 2.0
L = 50.0

# Vertical cylinder along Z, from z=0 to z=50, centered at the origin in XY
cyl_z = cq.Workplane("XY").circle(r).extrude(L)

# Horizontal cylinder along X, from x=0 to x=50, axis at z=0
cyl_x = cq.Workplane("YZ").circle(r).extrude(L)

result = cyl_z.union(cyl_x)
