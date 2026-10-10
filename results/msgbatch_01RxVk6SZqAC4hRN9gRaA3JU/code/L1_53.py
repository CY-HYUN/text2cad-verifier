import cadquery as cq

# Elliptical cylinder: major axis 80 (semi 40), minor axis 50 (semi 25), height 25
body = cq.Workplane("XY").ellipse(40.0, 25.0).extrude(25.0)

# 45° chamfer (0.8) on outer top ellipse edge
body = body.faces(">Z").edges().chamfer(0.8)

# Through hole: diameter 16 at (10, 0)
hole = cq.Workplane("XY").center(10.0, 0.0).circle(8.0).extrude(25.0)
result = body.cut(hole)
