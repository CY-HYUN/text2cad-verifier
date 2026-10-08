import cadquery as cq

# Overall plate dimensions
plate_length = 120.0   # X
plate_width = 50.0     # Y
plate_thickness = 6.0  # Z, extruded upward from the bottom face
corner_radius = 4.0

# Central slot dimensions
slot_length = 80.0
slot_width = 18.0      # end radius = 9

# Base plate, bottom face centred on the origin
plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Round the four vertical corner edges
plate = plate.edges("|Z").fillet(corner_radius)

# Cut the oval slot through the full thickness
slot = (
    cq.Workplane("XY")
    .slot2D(slot_length, slot_width, angle=0)
    .extrude(plate_thickness)
)

result = plate.cut(slot)
