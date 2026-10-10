import cadquery as cq

cyl = cq.Workplane("XY").circle(15.0).extrude(60.0)
cutter = cq.Workplane("XZ").center(0, 30.0).circle(5.0).extrude(50.0, both=True)
result = cyl.cut(cutter)
