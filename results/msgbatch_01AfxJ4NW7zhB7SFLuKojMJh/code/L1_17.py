import cadquery as cq

body = cq.Workplane("XY").box(60, 30, 20, centered=(True, False, True))
cut = cq.Workplane("XY").circle(20).extrude(10, both=True)
result = body.cut(cut)
