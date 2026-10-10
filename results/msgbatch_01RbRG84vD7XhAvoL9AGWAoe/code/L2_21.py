import cadquery as cq

# Base plate: 100 x 100 x 10 mm, bottom at z=0, top at z=10
plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))

# Sphere: diameter 40 mm, center on the plate's upper surface (z=10)
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))

# Union plate and sphere
body = plate.union(sphere)

# The sphere (radius 20) protrudes 10 mm below the plate bottom (z=-10).
# Cut the bottom flat at z=0, leaving a circular flat face (r = sqrt(20^2-10^2)).
cutter = cq.Workplane("XY").box(200, 200, 50, centered=(True, True, False)).translate((0, 0, -50))
result = body.cut(cutter)
