import cadquery as cq
import math

# Create the base rectangular prism
base = cq.Workplane("XY").box(100, 40, 30)

# Create semicircular cutout at the top edge along the length
# Create a 2D profile with a semicircle and extrude it
# The semicircle has radius 15mm at the center of the upper edge
sketch_semi = (
    cq.Sketch()
    .moveTo(-50, 0)
    .line(50, 0)
    .arc((50, 15), 15, 270, 90)
    .line(-50, 15)
    .close()
)
part = base.faces(">Z").workplane().sketch(sketch_semi).cutBlind(-15)

# Create rectangular groove on side face (60x10mm, depth 5mm)
# Select the front face and cut a centered 60x10mm rectangle inward 5mm
sketch_rect = cq.Sketch().rect(60, 10)
part = part.faces(">Y").workplane().sketch(sketch_rect).cutBlind(-5)

# Mirror the side groove to the opposite side
result = part.mirror("XZ")
