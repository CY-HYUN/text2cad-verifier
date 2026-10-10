import cadquery as cq
import math

# Elliptical base: major axis 80 (semi 40), minor axis 50 (semi 25), height 25
base = cq.Workplane("XY").ellipse(40, 25).extrude(25)

# Chamfer the outer top ellipse edge (before cutting hole so only the outer edge is selected)
base = base.faces(">Z").edges().chamfer(0.8)

# Offset through-hole, diameter 16 at (10, 0)
hole = cq.Workplane("XY").center(10, 0).circle(8).extrude(25)
result = base.cut(hole)
