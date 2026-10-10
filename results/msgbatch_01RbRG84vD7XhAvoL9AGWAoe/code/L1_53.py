import cadquery as cq

# Elliptical cylinder: 80 mm major axis (X), 50 mm minor axis (Y), 25 mm tall
body = cq.Workplane("XY").ellipse(40, 25).extrude(25)

# 0.8 mm 45-degree chamfer on the outer top ellipse edge
# (applied before the hole so only the outer edge is selected)
body = body.faces(">Z").edges().chamfer(0.8)

# 16 mm through-hole centred at (10, 0)
hole = (
    cq.Workplane("XY")
    .center(10, 0)
    .circle(8)
    .extrude(25)
)

result = body.cut(hole)
