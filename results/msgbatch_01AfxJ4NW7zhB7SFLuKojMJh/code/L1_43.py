import cadquery as cq

body = cq.Workplane("XY").box(100, 50, 30, centered=(False, True, False))
groove = cq.Workplane("XY").workplane(offset=10).box(100, 30, 20, centered=(False, True, False))
result = body.cut(groove)
