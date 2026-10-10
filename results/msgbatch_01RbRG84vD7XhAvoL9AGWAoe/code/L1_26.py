import cadquery as cq

sphere = cq.Workplane("XY").sphere(30)
cutter = cq.Workplane("XY").box(100, 100, 50, centered=(True, True, False)).translate((0, 0, 15))
result = sphere.cut(cutter)
