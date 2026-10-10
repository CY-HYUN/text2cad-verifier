import cadquery as cq
import math

# Main body: conical frustum (bottom Ø70, top Ø40, height 60)
cone = cq.Solid.makeCone(35, 20, 60, pnt=cq.Vector(0, 0, 0), dir=cq.Vector(0, 0, 1))
body = cq.Workplane("XY").add(cone)

# 45° chamfer, 2 mm, on the outer edge of the base (before the hole exists)
body = body.faces("<Z").edges().chamfer(2)

# Coaxial through-hole Ø20
hole = cq.Workplane("XY").circle(10).extrude(60)
result = body.cut(hole)
