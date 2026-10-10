import cadquery as cq

# Create the main rectangular plate
plate = cq.Workplane("XY").box(120, 40, 10, centered=True)

# Define hole positions
# The holes are 20mm from each end along the X-axis
# So they are at X = -50 and X = +50 (since the plate is 120mm long, centered at origin)
# Diameter is 10mm, so radius is 5mm

# Create the first hole at X = -50
hole1_x = -50
# Create the second hole at X = +50
hole2_x = 50

# Both holes are on the central axis (Y = 0, Z = center)
hole_y = 0
hole_radius = 5

# Create holes by drilling through the plate
result = plate.faces("+Z").workplane().pushPoints([
    (hole1_x, hole_y),
    (hole2_x, hole_y)
]).hole(hole_radius * 2)
