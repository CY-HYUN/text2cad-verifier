import cadquery as cq
import math

# Create the main rectangular block
# Dimensions: 60mm (X-length) × 30mm (Y-width) × 20mm (Z-thickness)
block = cq.Workplane("XY").box(60, 30, 20)

# Create a semicircular cylindrical cutout at the bottom center
# The semicircle has radius 20mm and its axis runs through the Z-direction (thickness)
# We need to cut a half-cylinder from the bottom

# Create a half-cylinder that extends through the entire thickness
# Position it at the center of the bottom surface
# The semicircle is in the XZ plane, centered at Y=0, Z at the bottom

# Create a cylinder and cut it in half
semicyl = cq.Workplane("XZ").cylinder(height=60, radius=20, centered=True).translate((0, 0, -10))

# Cut the semicircular hole from the block
# We'll use a different approach: create the half-cylinder as a solid to subtract
# Create a rectangular box that represents half the cylinder space, then use it for cutting

# Better approach: Create the half-cylinder by creating a cylinder and cutting it
cylinder_full = cq.Workplane("XY").cylinder(height=20, radius=20, centered=True)

# Position the cylinder at the bottom center and cut it
# The cylinder should be positioned with its axis along Y, at height Z = -10 (bottom surface)
result = block

# Create a half-cylinder cutout
# Use a combination approach: create a cylinder, position it, and cut half
# Translate cylinder to bottom center
cutout_cyl = cq.Workplane("XY").cylinder(height=20, radius=20, centered=True).translate((0, 0, -10))

# We need to cut only the upper half (semicircle facing up from bottom)
# Create the full cylinder first
full_cylinder = cq.Workplane("XY").cylinder(height=20, radius=20, centered=True).translate((0, 0, -10))

# To create a semicircular cutout, we cut with the cylinder and also intersect with the bottom half-space
# Actually, let's use a simpler method: create a half-cylinder directly

# Create semicircular cutout by rotating a semicircle around the Y-axis
# A semicircle in XZ plane, rotated to create the half-cylinder
sketch_profile = cq.Workplane("XZ").center(0, -10).moveTo(0, 0).circle(20).extrude(60, both=False)

# Cut the upper half only - use a box to limit the cut to the bottom half
# The semicircle should only cut into the bottom 20mm
half_space = cq.Workplane("XY").box(120, 120, 10).translate((0, 0, -15))
semicyl_cutout = cq.Workplane("XY").cylinder(height=20, radius=20, centered=True).translate((0, 0, -10))
semicyl_cutout = semicyl_cutout.intersect(half_space)

result = block.cut(semicyl_cutout)
