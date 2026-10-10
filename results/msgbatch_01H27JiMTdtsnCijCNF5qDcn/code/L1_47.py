import cadquery as cq

shaft = cq.Workplane("XY").circle(20.0).extrude(80.0)
cutter = cq.Workplane("XY").box(10.0, 6.0, 80.0, centered=(True, False, False)).translate((0, 15.0, 0))
result = shaft.cut(cutter)
