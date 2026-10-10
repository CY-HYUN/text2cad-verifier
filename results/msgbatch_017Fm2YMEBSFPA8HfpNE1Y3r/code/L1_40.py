import cadquery as cq
import math

# Create a workplane in the XZ plane for the profile
wp = cq.Workplane("XZ")

# Create the half-sectional profile by drawing lines
# Profile points in XZ plane: (r, z) where r is radius, z is axial position
profile = (
    wp
    .moveTo(0, 0)  # Start at origin (r=0, z=0)
    .lineTo(15, 0)  # Radius 15mm at z=0
    .lineTo(15, 20)  # Vertical line to z=20
    .lineTo(7.5, 20)  # Step down to radius 7.5mm
    .lineTo(7.5, 40)  # Horizontal line to z=40 (middle section)
    .lineTo(15, 40)  # Step up to radius 15mm
    .lineTo(15, 60)  # Vertical line to z=60
    .lineTo(0, 60)  # Return to axis at z=60
    .close()  # Close the profile
    .revolve(360)  # Revolve 360 degrees around the Z-axis
)

result = profile
