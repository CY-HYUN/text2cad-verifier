import cadquery as cq

r = 10
L = 50

# Cylinder along X axis (x from 0 to 50), axis at y=0, z=0
cyl_x = cq.Workplane("YZ").circle(r).extrude(L)

# Cylinder along Y axis (y from 0 to 50), axis at x=0, z=0
cyl_y = cq.Workplane("XZ").circle(r).extrude(-L)

result = cyl_x.union(cyl_y)
