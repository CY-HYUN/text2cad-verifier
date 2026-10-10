import cadquery as cq

block = cq.Workplane("XY").rect(90, 50).extrude(30)

groove = (cq.Workplane("XY").workplane(offset=30)
          .rect(90, 20).extrude(-12))
body = block.cut(groove)

result = (body.edges("|X")
          .edges(cq.selectors.BoxSelector((-50, -11, 17.5), (50, 11, 18.5)))
          .fillet(2.0))
