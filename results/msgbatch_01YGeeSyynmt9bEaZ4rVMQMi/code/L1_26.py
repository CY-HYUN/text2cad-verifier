import cadquery as cq

sphere = cq.Workplane("XY").sphere(30.0)
cutter = cq.Workplane("XY").box(100, 100, 100, centered=(True, True, False)).translate((0, 0, 15.0))
result = sphere.cut(cutter)
