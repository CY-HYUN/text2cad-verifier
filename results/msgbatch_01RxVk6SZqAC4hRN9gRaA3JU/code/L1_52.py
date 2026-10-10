import cadquery as cq

# Plate: 120 x 50 rectangle centered on origin, extruded 6 mm
plate = cq.Workplane("XY").rect(120.0, 50.0).extrude(6.0)

# Fillet the four vertical outer corner edges, R4
plate = plate.edges("|Z").fillet(4.0)

# Through slot: overall length 80, width 18, centered, along X
result = (
    plate.faces(">Z").workplane()
    .slot2D(80.0, 18.0, 0)
    .cutThruAll()
)
