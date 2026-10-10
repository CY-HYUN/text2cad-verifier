import cadquery as cq
import math

# Create the initial cylinder
result = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)

# Create a rectangular cut sketch in the front view (XZ plane)
# The rectangle is 5mm wide, centered horizontally
# Inner edge is 1mm from the axis (so from radius 1mm to radius 6mm)
# We'll cut this rectangle rotated 360 degrees to create a groove

# The groove parameters:
# - Width: 5mm (from 1mm to 6mm radius)
# - Height: full length of cylinder (50mm)
# - This creates a deep groove leaving a 2mm diameter (1mm radius) central shaft

# Create the groove by subtracting a rectangular solid rotated around
# We need to cut a rectangular section that spans from 1mm to 6mm radius
# We'll do this by creating a box and rotating it around the Z axis

# Create a rectangular cut box positioned to cut the groove
# Box dimensions: 10mm wide (to cover the full diameter sweep), 50mm tall, 5mm deep
# Positioned so it cuts from radius 1mm to 6mm

# Create the groove by positioning a rectangular cutting tool
cut_box = cq.Workplane("XY").box(10, 50, 5, centered=True)

# We need to position this box at the right radial position (1mm to 6mm from center)
# Offset the box to start at radius 1mm
offset_distance = 3.5  # Center of the 5mm wide section is at 1 + 2.5 = 3.5mm from axis
cut_box = cut_box.translate((offset_distance, 0, 0))

# Perform a circular pattern (360 degree rotation) of this cut
# Actually, for a continuous groove, we need to cut the material differently
# Let's create a solid that represents what remains after the groove

# Better approach: create the groove using a subtraction of a rectangular extrusion
# rotated around the cylinder axis

# Create a rectangular profile for the groove
# This rectangle is 5mm wide (radially), extends full height
groove_profile = cq.Workplane("ZX").rect(5, 50, centered=True)
groove_solid = groove_profile.extrude(1)  # Extrude outward

# Position the groove at the correct radius (1mm from axis, extending 5mm outward)
# The groove needs to be positioned at radius 1mm to 6mm
groove_solid = groove_solid.translate((3.5, 0, 0))

# Create the final shape by cutting the groove all around (360 degrees)
# We'll do this by cutting multiple times or using a polar array approach
result = result.cut(groove_solid)

# For a true 360-degree groove, we would need to sweep or create an annular cut
# Let's use a different approach: create the groove by subtracting an annular section

# Clear and restart with better approach
result = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)

# Create groove by cutting an annular section from 1mm to 6mm radius, full height
# This is done by creating a cylinder of radius 6mm and subtracting cylinder of radius 1mm
# But only for a certain angular range, then rotating

# Simpler approach: Create the final shape directly
# Keep a 1mm radius central shaft, and cut the outer groove
groove_outer = cq.Workplane("XY").cylinder(height=50, radius=6, centered=True)
groove_inner = cq.Workplane("XY").cylinder(height=50, radius=1, centered=True)
groove = groove_outer.cut(groove_inner)

# Now we have the groove form, we need to subtract it from the main cylinder
# positioned correctly
result = cq.Workplane("XY").cylinder(height=50, radius=10, centered=True)
result = result.cut(groove)

