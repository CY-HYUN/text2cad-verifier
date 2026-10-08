import cadquery as cq

body = cq.Workplane("XY").ellipse(40, 25).extrude(25)
body = body.faces(">Z").edges("not %CIRCLE").chamfer(0.8) if False else body

# chamfer outer top ellipse edge before hole
body = cq.Workplane("XY").ellipse(40, 25).extrude(25)
body = body.faces(">Z").edges().chamfer(0.8)

hole = cq.Workplane("XY").center(10, 0).circle(8).extrude(25)
result = body.cut(hole)
