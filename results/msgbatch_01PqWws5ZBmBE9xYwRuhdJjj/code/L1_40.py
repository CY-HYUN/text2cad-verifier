import cadquery as cq
import math

# Create a new workplane with XY plane as base (Z-axis pointing upwards)
wp = cq.Workplane("XY")

# Create a half-sectional profile in the XZ plane for revolution
# This profile will be revolved around the Z-axis
# Define the profile as a series of points along the Z-axis (axial direction)
# and the radial distance from the Z-axis

# Profile points: (z, r) where z is along axis, r is radius
# The profile goes from z=0 to z=60 with the specified radii

# Start with a sketch on the XZ plane (using XY workplane rotated)
sketch = (
    cq.Sketch()
    .moveTo(0, 0)  # Start at origin
    .lineTo(15, 0)  # First radius 15mm at z=0
    .lineTo(15, 20)  # Vertical line to z=20
    .lineTo(7.5, 20)  # Step down to radius 7.5mm
    .lineTo(7.5, 40)  # Horizontal line to z=40 (middle section length 20mm)
    .lineTo(15, 40)  # Step up to radius 15mm
    .lineTo(15, 60)  # Vertical line to z=60
    .lineTo(0, 60)  # Return to axis at z=60
    .close()  # Close the profile
)

# Create a workplane and apply the sketch in the XZ plane
# We need to work in XZ plane, so we'll use a different approach
# Create the profile using direct geometry in the XZ plane

# Use Plane XZ by rotating the default plane
wp_xz = cq.Workplane("XZ")

# Create the profile for revolution
profile = (
    wp_xz
    .moveTo(0, 0)  # Origin at (r=0, z=0)
    .lineTo(15, 0)  # Radius 15 at z=0
    .lineTo(15, 20)  # Extend to z=20
    .lineTo(7.5, 20)  # Step to radius 7.5
    .lineTo(7.5, 40)  # Extend to z=40
    .lineTo(15, 40)  # Step back to radius 15
    .lineTo(15, 60)  # Extend to z=60
    .lineTo(0, 60)  # Return to axis
    .close()  # Close the profile
    .revolve(360)  # Revolve 360 degrees around the Z-axis
)

result = profile
