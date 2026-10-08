import cadquery as cq

# Cube 40x40x40, base on XY plane, extruded upward along +Z
result = (
    cq.Workplane("XY")
    .rect(40.0, 40.0)
    .extrude(40.0)
)

# Through hole Ø20 from the top face
result = (
    result.faces(">Z").workplane()
    .circle(10.0)
    .cutThruAll()
)

# Counterbore Ø30, 10 mm deep, from the top face
result = (
    result.faces(">Z").workplane()
    .circle(15.0)
    .cutBlind(-10.0)
)
