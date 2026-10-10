import cadquery as cq
import math

# Create a workplane on the front plane
wp = cq.Workplane("front")

# Draw the profile sketch for revolving around the Y-axis (vertical axis)
# The profile will be drawn in the XY plane, with X as radius and Y as height
# Start from the bottom-left corner and trace counterclockwise

# Profile points (x, y) where x is radial distance, y is height
# Tube: inner radius 15mm, outer radius 20mm, length 100mm
# Bottom flange at y=0 to y=10mm, width 5mm (extends from r=20 to r=25)
# Retaining ring at y=47.5 to y=52.5mm, width 5mm (from r=20 to r=25)
# Top flange at y=90 to y=100mm, width 5mm (from r=20 to r=25)

profile = wp.moveTo(15, 0)  # Inner radius at bottom
profile = profile.lineTo(20, 0)  # Outer radius at bottom (outer wall)
profile = profile.lineTo(25, 0)  # Flange outer radius
profile = profile.lineTo(25, 10)  # Bottom flange height
profile = profile.lineTo(20, 10)  # Back to outer wall
profile = profile.lineTo(20, 47.5)  # Tube to retaining ring
profile = profile.lineTo(25, 47.5)  # Retaining ring outer radius
profile = profile.lineTo(25, 52.5)  # Retaining ring height
profile = profile.lineTo(20, 52.5)  # Back to outer wall
profile = profile.lineTo(20, 90)  # Tube to top flange
profile = profile.lineTo(25, 90)  # Top flange outer radius
profile = profile.lineTo(25, 100)  # Top flange height
profile = profile.lineTo(20, 100)  # Back to outer wall
profile = profile.lineTo(15, 100)  # Inner radius at top
profile = profile.lineTo(15, 52.5)  # Inner wall down to retaining ring
profile = profile.lineTo(15, 47.5)  # Inner wall through retaining ring
profile = profile.lineTo(15, 10)  # Inner wall down to bottom flange
profile = profile.lineTo(15, 0)  # Back to start
profile = profile.close()  # Close the profile

# Revolve the profile 360 degrees around the Y-axis (vertical centerline)
result = profile.revolve(360, axisStart=(0, 0), axisEnd=(0, 1))
