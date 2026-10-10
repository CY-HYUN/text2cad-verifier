import cadquery as cq

# Base cylinder: diameter 40, height 40
body = cq.Workplane("XY").circle(20.0).extrude(40.0)

# Through hole: diameter 10, cut through the entire part
body = body.cut(cq.Workplane("XY").circle(5.0).extrude(40.0))

# Counterbore: diameter 20, depth 10 from the top surface (z = 40 down to z = 30)
body = body.cut(cq.Workplane("XY").workplane(offset=30.0).circle(10.0).extrude(10.0))

result = body
