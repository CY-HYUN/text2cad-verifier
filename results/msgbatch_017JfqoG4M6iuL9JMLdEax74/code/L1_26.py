import cadquery as cq

sphere = cq.Workplane("XY").sphere(30)
cutter = cq.Workplane("XY").box(100, 100, 50).translate((0, 0, 15 + 25))
result = sphere.cut(cutter)
