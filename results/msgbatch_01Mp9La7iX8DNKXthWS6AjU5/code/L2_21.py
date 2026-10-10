import cadquery as cq

plate = cq.Workplane("XY").box(100, 100, 10, centered=(True, True, False))
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 10))
merged = plate.union(sphere)

cutter = cq.Workplane("XY").workplane(offset=-20).rect(60, 60).extrude(20)
result = merged.cut(cutter)
