import cadquery as cq

plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))
body = plate.union(sphere)

# cut the bottom flat at z=0 (removes the part of the sphere protruding below the plate)
cutter = cq.Workplane("XY").box(200, 200, 50, centered=(True, True, False)).translate((0, 0, -50))
result = body.cut(cutter)
