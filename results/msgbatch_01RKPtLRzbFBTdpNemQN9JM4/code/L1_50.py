import cadquery as cq

r = 10.0
L = 50.0

# Cylinder along X, from x=0 to x=50
cyl_x = cq.Workplane("YZ").circle(r).extrude(L)

# Cylinder along Y, from y=0 to y=50
cyl_y = cq.Workplane("XZ").circle(r).extrude(-L)

result = cyl_x.union(cyl_y)
