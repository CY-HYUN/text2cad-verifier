import cadquery as cq

plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))
body = plate.union(sphere)
cutter = cq.Workplane("XY").workplane(offset=-30).rect(60, 60).extrude(30)
result = body.cut(cutter)
