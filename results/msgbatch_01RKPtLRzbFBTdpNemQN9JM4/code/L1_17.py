import cadquery as cq

box = cq.Workplane("XY").box(60, 30, 20, centered=(True, False, False))
cyl = cq.Workplane("XY").center(0, 0).circle(20).extrude(20)
result = box.cut(cyl)
