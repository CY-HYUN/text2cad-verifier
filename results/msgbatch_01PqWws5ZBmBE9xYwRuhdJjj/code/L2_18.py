import cadquery as cq
import math

# Create the base rectangular prism
base = cq.Workplane("XY").box(100, 40, 30)

# Create a semicircle cutout at the upper edge along the length
# The semicircle is at the center of the upper edge with radius 15mm
# We'll create this by using a sketch on the end face
sketch1 = cq.Sketch().arc((0, 15), 15, 180, 0).line((15, 15), (-15, 15)).close()
# Pad the sketch through the entire length (100mm)
part = base.faces(">Z").workplane().sketch(sketch1).pad(100)

# Actually, let's approach this differently - create the semicircle cutout properly
# Start fresh and build the part step by step
base = cq.Workplane("XY").box(100, 40, 30)

# Create semicircular cutout at the top edge
# Use a sketch on the top face at the center of one edge
sketch_semi = cq.Sketch().arc((0, 20), 15, 180, 0).line((15, 20), (-15, 20)).close()
semi_cut = base.faces(">Z").workplane(origin=(0, 20, 15)).sketch(sketch_semi).cutBlind(-15)

# Create rectangular groove on side face (60x10mm, depth 5mm)
# Select the front face (+Y direction) and center the 60x10mm rectangle
part_with_groove = semi_cut.faces(">Y").workplane().center(0, 0)
sketch_rect = cq.Sketch().rect(60, 10)
part_with_groove = semi_cut.faces(">Y").workplane().sketch(sketch_rect).cutBlind(-5)

# Mirror the side groove to the other side (opposite face in -Y direction)
result = part_with_groove.mirror("XZ")
