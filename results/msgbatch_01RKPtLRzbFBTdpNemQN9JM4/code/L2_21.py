import cadquery as cq

plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))
union = plate.union(sphere)
clip = cq.Workplane("XY").box(200, 200, 40, centered=(True, True, False))
result = union.intersect(clip)
