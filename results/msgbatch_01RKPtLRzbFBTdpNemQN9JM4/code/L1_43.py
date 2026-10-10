import cadquery as cq

body = cq.Workplane("XY").box(100, 50, 30, centered=(True, True, False))
groove = (cq.Workplane("XY").workplane(offset=10)
          .rect(100, 30).extrude(20))
result = body.cut(groove)
