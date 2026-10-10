import cadquery as cq

# Dimensions (mm)
outer_diameter = 90.0
thickness = 15.0
square_side = 30.0

# Cylindrical flange body along Z
body = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(thickness)

# Square through-hole centred on the cylinder axis
hole = (
    cq.Workplane("XY")
    .rect(square_side, square_side)
    .extrude(thickness)
)

result = body.cut(hole)
