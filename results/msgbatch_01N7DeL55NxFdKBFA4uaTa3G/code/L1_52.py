import cadquery as cq

# Base plate: 120 x 50 centered rectangle, 6 mm thick
plate = cq.Workplane("XY").rect(120.0, 50.0).extrude(6.0)

# Fillet the four vertical outer corner edges (R4)
plate = plate.edges("|Z").fillet(4.0)

# Through slot on top face: total length 80, width 18, along X, centered
result = (
    plate.faces(">Z").workplane()
    .slot2D(80.0, 18.0, 0)
    .cutThruAll()
)
