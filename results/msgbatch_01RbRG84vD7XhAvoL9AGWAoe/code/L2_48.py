import cadquery as cq

L = 50.0
R = 30.0

cube = cq.Workplane("XY").box(L, L, L, centered=False)
sphere = cq.Workplane("XY").sphere(R)  # centered at origin vertex (0,0,0)

result = cube.cut(sphere)
