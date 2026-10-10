import cadquery as cq

# Base plate 120 x 50 x 6, centered on the XY origin
plate = cq.Workplane("XY").rect(120.0, 50.0).extrude(6.0)

# Fillet the four outer vertical corner edges (radius 4)
plate = plate.edges("|Z").fillet(4.0)

# Through slot on the top face: total length 80, width 18, along X, centered
plate = (
    plate.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    .slot2D(80.0, 18.0, 0)
    .cutThruAll()
)

result = plate
