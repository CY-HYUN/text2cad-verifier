import cadquery as cq
import math

# Create the top plate
top_plate = cq.Workplane("XY").box(100, 100, 5)

# Create the four cylindrical legs
leg_height = 50
leg_diameter = 10
leg_radius = leg_diameter / 2

# Positions for the four legs (at corners, inset from edges)
leg_positions = [
    (-35, -35),  # Bottom-left
    (35, -35),   # Bottom-right
    (35, 35),    # Top-right
    (-35, 35),   # Top-left
]

# Create a single leg
leg = cq.Workplane("XY").cylinder(leg_height, leg_radius)

# Create all four legs by positioning them
legs = cq.Workplane("XY")
for x, y in leg_positions:
    leg_at_pos = leg.translate((x, y, -leg_height/2 - 2.5))
    legs = legs.union(leg_at_pos)

# Create the base frame (outer square 100x100, inner square 80x80, thickness 5)
outer_base = cq.Workplane("XY").box(100, 100, 5)
inner_cutout = cq.Workplane("XY").box(80, 80, 5.5)  # Slightly taller for clean cut

base_frame = outer_base.cut(inner_cutout)
base_frame = base_frame.translate((0, 0, -leg_height - 2.5))

# Create corner supports (small connecting pieces at inner corners beneath top plate)
support_size = 15
support_height = 2.5
support_positions = [
    (-42.5, -42.5),  # Bottom-left
    (42.5, -42.5),   # Bottom-right
    (42.5, 42.5),    # Top-right
    (-42.5, 42.5),   # Top-left
]

corner_supports = cq.Workplane("XY")
for x, y in support_positions:
    support = cq.Workplane("XY").box(support_size, support_size, support_height)
    support = support.translate((x, y, -support_height/2 - 2.5))
    corner_supports = corner_supports.union(support)

# Assemble the complete table
result = top_plate.union(legs).union(base_frame).union(corner_supports)
