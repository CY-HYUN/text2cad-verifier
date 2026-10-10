import cadquery as cq
import math

# Create the base plate
base_plate = cq.Workplane("XY").box(100, 100, 10)

# Create a sphere with radius 20mm centered at the top surface center
# The top surface is at z=5 (half of 10mm height)
sphere = cq.Workplane("XY").sphere(20).translate((0, 0, 5))

# Merge the sphere with the base plate
merged = base_plate.union(sphere)

# Create a cutting box to remove the protruding part below the bottom of the plate
# The bottom surface of the base plate is at z=-5
# We need to cut everything below z=-5
# Create a large rectangular box that extends below the bottom surface
cut_box = cq.Workplane("XY").box(200, 200, 20).translate((0, 0, -15))

# Cut the merged part with the box to flatten the bottom
result = merged.cut(cut_box)
