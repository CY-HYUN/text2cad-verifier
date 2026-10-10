import cadquery as cq
import math

# Create a new workplane with the XY plane as the bottom sketch plane
workplane = cq.Workplane("XY")

# Switch to the YZ plane for drawing the semicircular pipe cross-section
# We need to work in the YZ plane, so we'll create the profile there
workplane = workplane.workplane(offset=0).transformed(offset=(0, 0, 0))

# Create the semicircular ring profile in the YZ plane
# Start by creating a workplane in the YZ plane
profile = cq.Workplane("YZ")

# Draw the outer semicircular arc (radius 30 mm)
# A semicircle from top to bottom in the YZ plane
outer_arc = profile.moveTo(0, 0).radiusArc((0, 0), 30, 0, 180)

# Draw the diameter line at the bottom (from (0, -30) to (0, 30) but we're at bottom)
# This closes the outer semicircle
# Actually, for a semicircular ring, we need:
# 1. Outer arc from one end of diameter to the other
# 2. Inner arc going back
# 3. Diameter line to close

# Let's create the profile more carefully
# In YZ plane: Y is horizontal, Z is vertical
# Create outer semicircle: from Y=30, Z=0 going up and around to Y=-30, Z=0
profile = cq.Workplane("YZ").moveTo(30, 0)

# Create outer arc (top half of circle with radius 30)
profile = profile.radiusArc((-30, 0), 30)

# Now we're at (-30, 0), need to go to (-20, 0) to start inner arc
profile = profile.lineTo(-20, 0)

# Create inner arc going back (bottom half of circle with radius 20)
profile = profile.radiusArc((20, 0), 20)

# Close the profile back to start point
profile = profile.lineTo(30, 0).close()

# Get the face from this profile
face = profile.faces(">Z").val()

# Now extrude this face 100 mm in the +X direction
# We need to extrude the closed profile
profile_wire = profile.val()

# Create a solid by extruding the profile in the X direction
result = cq.Workplane("YZ").moveTo(30, 0).radiusArc((-30, 0), 30).lineTo(-20, 0).radiusArc((20, 0), 20).lineTo(30, 0).close().extrude(100, "normal")

# Alternative approach: use the profile and extrude it
# Create the 2D profile as a closed wire
result = (
    cq.Workplane("YZ")
    .moveTo(30, 0)
    .radiusArc((-30, 0), 30)
    .lineTo(-20, 0)
    .radiusArc((20, 0), 20)
    .lineTo(30, 0)
    .close()
    .extrude(100)
)
