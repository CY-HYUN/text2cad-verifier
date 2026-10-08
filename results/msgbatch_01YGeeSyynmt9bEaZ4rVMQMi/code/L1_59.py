import cadquery as cq

# Base cylinder: diameter 60, height 80
body = cq.Workplane("XY").circle(30.0).extrude(80.0)

# Groove profile in XZ plane (radial 27..30, Z 35..45), revolved 360 deg about Z
groove = (
    cq.Workplane("XZ")
    .moveTo(27.0, 35.0)
    .lineTo(30.0, 35.0)
    .lineTo(30.0, 45.0)
    .lineTo(27.0, 45.0)
    .close()
    .revolve(360.0, (0, 0, 0), (0, 1, 0))
)
body = body.cut(groove)

# Fillet the outer circular edges on both sides of the groove
sel = [
    e for e in body.edges().vals()
    if e.geomType() == "CIRCLE"
    and abs(e.radius() - 30.0) < 1e-6
    and 1.0 < e.Center().z < 79.0
]
result = body.newObject(sel).fillet(1.0)
