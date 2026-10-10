import cadquery as cq
import math

# Create a workplane in the YZ plane
# We'll build the semicircular ring profile there
profile = cq.Workplane("YZ")

# Start at the right end of the diameter (30, 0)
# Draw outer semicircle arc to the left end (-30, 0)
# radiusArc takes (endPoint, radius) - the radius is the arc radius
profile = profile.moveTo(30, 0).radiusArc((-30, 0), 30)

# Now at (-30, 0), move inward to start the inner arc at (-20, 0)
profile = profile.lineTo(-20, 0)

# Draw inner semicircle arc back to (20, 0)
profile = profile.radiusArc((20, 0), 20)

# Close the profile back to the starting point (30, 0)
profile = profile.lineTo(30, 0).close()

# Extrude the profile 100 mm in the X direction (+X)
result = profile.extrude(100)
