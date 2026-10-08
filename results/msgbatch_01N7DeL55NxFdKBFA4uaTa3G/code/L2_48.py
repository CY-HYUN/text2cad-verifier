import cadquery as cq

cube = cq.Workplane("XY").box(50, 50, 50, centered=False)
sphere = cq.Workplane("XY").sphere(30)  # centered at vertex (0,0,0)
result = cube.cut(sphere)
