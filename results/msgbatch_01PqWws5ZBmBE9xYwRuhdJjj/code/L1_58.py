import cadquery as cq
import math

# Create a centered rectangle 90.0 x 50.0 in the XY plane and extrude it 30.0
result = cq.Workplane("XY").rect(90.0, 50.0).extrude(30.0)

# Select the top face for sketching
result = result.faces(">Z").workplane()

# Draw a centered rectangular groove profile: length 90.0, width 20.0
result = result.rect(90.0, 20.0).extrude(-12.0, combine="cut")

# Apply a fillet with radius 2.0 to the two long intersection lines at the bottom of the groove
# The intersection lines are the edges where the groove meets the bottom of the groove
# We need to select the edges that form the long sides of the groove at the bottom
result = result.edges("|Z").fillet(2.0)

