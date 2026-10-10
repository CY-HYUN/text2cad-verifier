import cadquery as cq
import math

# Create a regular octagon with circumscribed circle diameter of 40mm
# Circumradius = 20mm
circumradius = 20
sides = 8

# Calculate vertices of regular octagon
vertices = []
for i in range(sides):
    angle = 2 * math.pi * i / sides
    x = circumradius * math.cos(angle)
    y = circumradius * math.sin(angle)
    vertices.append((x, y))

# Create the octagon and extrude it by 60mm
octagon = cq.Workplane("XY").polygon(sides, circumradius).extrude(60)

# Create a cutting profile for sharpening the top (45-degree angle triangular cut)
# The cutting profile is in the XZ plane (front view)
# Triangle: base at top (y=60), apex at center (y=0), at circumradius distance (x=20)
cutting_profile_sharp = cq.Workplane("XZ").polyline([
    (circumradius, 60),  # top corner
    (0, 0),              # center at bottom
    (circumradius, 60)   # back to start
]).close()

# Revolve the sharp profile around the Z axis (central axis)
sharp_cut = cutting_profile_sharp.revolve(360, axisEnd=(0, 0, 60))
octagon = octagon.cut(sharp_cut)

# Create rectangular profile for annular groove at midpoint height (30mm)
# Profile: 5mm wide, 2mm from edge
# Distance from center: circumradius - 2 = 18mm
groove_distance = circumradius - 2
groove_width = 5
groove_height = 30  # midpoint

# Rectangular profile in XZ plane at y=groove_distance
# Rectangle from (groove_distance, groove_height - groove_width/2) to (groove_distance, groove_height + groove_width/2)
cutting_profile_groove = cq.Workplane("XZ").polyline([
    (groove_distance, groove_height - groove_width/2),
    (groove_distance, groove_height + groove_width/2),
    (groove_distance + 0.1, groove_height + groove_width/2),
    (groove_distance + 0.1, groove_height - groove_width/2)
]).close()

# Revolve the groove profile around the Z axis
groove_cut = cutting_profile_groove.revolve(360, axisEnd=(0, 0, 60))
result = octagon.cut(groove_cut)
