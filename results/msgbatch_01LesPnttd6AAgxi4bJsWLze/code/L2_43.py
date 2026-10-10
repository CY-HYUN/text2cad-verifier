import cadquery as cq
import math

# Create the square frame base
# Outer square: 60mm x 60mm
# Inner square hole: 40mm x 40mm

# Start with a 60mm x 60mm square, 10mm tall (arbitrary height for the frame)
frame_height = 10

# Create the outer square
outer_square = cq.Workplane("XY").box(60, 60, frame_height, centered=True)

# Create the inner square hole (40mm x 40mm)
# We'll subtract a square from the frame
inner_square = cq.Workplane("XY").box(40, 40, frame_height + 2, centered=True)

# Subtract the inner square from the outer square to create the frame
frame = outer_square.cut(inner_square)

# Create the cylinder
# Diameter: 40mm (radius: 20mm)
# Height: 20mm
# Centered within the square hole

cylinder = cq.Workplane("XY").cylinder(20, 20, centered=True)

# Position the cylinder so it sits on top of the frame (or merged with it)
# The cylinder should be positioned so its bottom is at the top of the frame
# Frame top is at frame_height/2, cylinder bottom should be positioned accordingly
# Since we want them to form a single solid, we'll union them

# Move cylinder up so its bottom aligns with the frame top
cylinder = cylinder.translate((0, 0, frame_height/2 + 10))

# Combine the frame and cylinder into a single solid
result = frame.union(cylinder)
