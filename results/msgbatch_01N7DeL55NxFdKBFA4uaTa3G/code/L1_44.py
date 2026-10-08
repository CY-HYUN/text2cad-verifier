import cadquery as cq

# Base cube 40 x 40 x 40, sitting on XY plane, Z up
result = (
    cq.Workplane("XY")
    .rect(40.0, 40.0)
    .extrude(40.0)
)

# Through hole (diameter 20) from top face
result = (
    result.faces(">Z").workplane()
    .circle(10.0)
    .cutThruAll()
)

# Counterbore (diameter 30, depth 10) from top face
result = (
    result.faces(">Z").workplane()
    .circle(15.0)
    .cutBlind(-10.0)
)
