import cadquery as cq

box = cq.Workplane("XY").box(60, 30, 30, centered=(True, True, False))

ell = (cq.Workplane("XZ").center(0, 0).ellipse(20, 15).extrude(20, both=True))
result = box.cut(ell)

hole = cq.Workplane("XY").workplane(offset=30).circle(5).extrude(-30)
result = result.cut(hole)
