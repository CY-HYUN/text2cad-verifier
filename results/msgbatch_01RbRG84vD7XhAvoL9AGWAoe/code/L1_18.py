import cadquery as cq

r = 15.0
L = 60.0

# Cylinder along X, centered at origin
cyl = cq.Workplane("YZ").circle(r).extrude(L).translate((-L / 2, 0, 0))

# Spheres at each end (union yields hemispherical caps)
s1 = cq.Workplane("XY").sphere(r).translate((L / 2, 0, 0))
s2 = cq.Workplane("XY").sphere(r).translate((-L / 2, 0, 0))

result = cyl.union(s1).union(s2)
