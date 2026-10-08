import cadquery as cq

disc = cq.Workplane("XY").circle(30).extrude(10)
cutter = cq.Workplane("XY").center(30, 0).circle(10).extrude(10)
result = disc.cut(cutter)
