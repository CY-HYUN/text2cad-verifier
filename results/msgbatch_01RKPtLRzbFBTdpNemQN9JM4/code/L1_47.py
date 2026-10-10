import cadquery as cq

shaft = cq.Workplane("XY").circle(20).extrude(80)
groove = cq.Workplane("XY").box(7, 10, 40, centered=(True, True, False)).translate((18.5, 0, 20))
result = shaft.cut(groove)
