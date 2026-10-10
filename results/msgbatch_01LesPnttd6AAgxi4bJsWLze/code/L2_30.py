import cadquery as cq
import math

# Create the main rectangular body
main_body = cq.Workplane("XY").box(60, 30, 30)

# Create a semi-cylinder to cut out from the bottom
# The semi-cylinder should be along the long axis (60mm direction)
# Radius should be half the height (15mm) to create the arch
semi_cylinder = (
    cq.Workplane("XZ")
    .circle(15)  # radius of 15mm (half of 30mm height)
    .extrude(60)  # extend along the 60mm length
)

# Position the semi-cylinder at the bottom center
# We need to move it down so it cuts from the bottom surface
semi_cylinder = semi_cylinder.translate((0, -15, -15))

# Cut the semi-cylinder from the main body
result = main_body.cut(semi_cylinder)

# Add vertical holes through the object
# Holes positioned at corners to allow contact at corners
# Create holes at the four corner positions
hole_radius = 2.5  # 5mm diameter holes
hole_depth = 30  # goes through the entire height

# Define hole positions relative to the center of the 60x30 rectangle
# Corners are at (±30, ±15) from center
hole_positions = [
    (25, 10),   # one corner area
    (25, -10),  # another corner area
    (-25, 10),  # another corner area
    (-25, -10)  # last corner area
]

# Drill holes through the object
for x, y in hole_positions:
    hole = cq.Workplane("Z").circle(hole_radius).extrude(-30)
    hole = hole.translate((x, y, 15))
    result = result.cut(hole)

# Ensure the result is a valid solid
result = result.val()
