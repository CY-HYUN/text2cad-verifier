import cadquery as cq

# Base plate: 100 x 100 x 10 mm, bottom at z=0, top at z=10
plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))

# Sphere: diameter 40 mm, center on the plate's upper surface
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))

body = plate.union(sphere)

# Cut the bottom flat at z=0, removing the part of the sphere that protrudes below the plate
keep = cq.Workplane("XY").box(200, 200, 100, centered=(True, True, False))
result = body.intersect(keep)
