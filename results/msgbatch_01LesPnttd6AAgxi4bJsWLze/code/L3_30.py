import cadquery as cq
import math

# Create the main base block
base = cq.Workplane("XY").box(150, 100, 30, centered=True)

# Add the dovetail guide rail on top
# The dovetail is a trapezoidal protrusion with bottom width 60mm, height 15mm, side angles 60 degrees
# Calculate the top width based on 60-degree angles
height_dovetail = 15
bottom_width_dovetail = 60
angle_rad = math.radians(60)
offset = height_dovetail / math.tan(angle_rad)
top_width_dovetail = bottom_width_dovetail + 2 * offset

# Create the dovetail trapezoid in 2D
dovetail_face = (
    cq.Workplane("XZ")
    .moveTo(-bottom_width_dovetail / 2, 0)
    .lineTo(-top_width_dovetail / 2, height_dovetail)
    .lineTo(top_width_dovetail / 2, height_dovetail)
    .lineTo(bottom_width_dovetail / 2, 0)
    .close()
    .extrude(150)
)

# Position the dovetail on top of the base
dovetail = dovetail_face.translate((0, 0, 15))

# Combine base with dovetail
part = base.union(dovetail)

# Add T-slots on both sides (150x30 surfaces)
# T-slot: mouth width 10mm, internal width 16mm
# Create T-slot profile: rectangular mouth on outside, wider inside
t_slot_depth = 10
t_slot_mouth = 10
t_slot_internal = 16

# T-slot on one side (Y = -50)
t_slot_profile = (
    cq.Workplane("XZ")
    .moveTo(-t_slot_mouth / 2, 0)
    .lineTo(-t_slot_internal / 2, 2)
    .lineTo(-t_slot_internal / 2, t_slot_depth)
    .lineTo(t_slot_internal / 2, t_slot_depth)
    .lineTo(t_slot_internal / 2, 2)
    .lineTo(t_slot_mouth / 2, 0)
    .close()
)

# Create T-slot as a cut (extrude profile along length)
t_slot_cut = t_slot_profile.extrude(150)
t_slot_cut_left = t_slot_cut.translate((0, -50, -10))
t_slot_cut_right = t_slot_cut.translate((0, 50, -10))

# Remove T-slots from part
part = part.cut(t_slot_cut_left)
part = part.cut(t_slot_cut_right)

# Add central countersunk hole on dovetail top surface
# Larger hole: diameter 40mm, depth 5mm
# Smaller hole: diameter 30mm, through
central_hole = (
    cq.Workplane("XY")
    .cylinder(5, 20, centered=True)  # countersink: 40mm diameter, 5mm depth
    .translate((0, 0, 30))
)
part = part.cut(central_hole)

# Add the main hole through the dovetail (30mm diameter)
main_hole = cq.Workplane("XY").cylinder(100, 15, centered=True).translate((0, 0, 0))
part = part.cut(main_hole)

# Add four corner mounting holes (8mm diameter, countersunk)
corner_positions = [
    (-65, -40),
    (65, -40),
    (-65, 40),
    (65, 40),
]

for x, y in corner_positions:
    # Countersunk hole: 8mm diameter main hole, slightly larger countersink
    corner_hole = cq.Workplane("XY").cylinder(30, 4, centered=True).translate((x, y, -15))
    part = part.cut(corner_hole)

# Add oil groove relief at the root of dovetail (2mm wide, 1mm deep on both sides)
# These are at the sides of the dovetail base
oil_groove_width = 2
oil_groove_depth = 1
oil_groove_position_y = (bottom_width_dovetail / 2)

# Left oil groove
left_groove = cq.Workplane("XZ").box(150, oil_groove_width, oil_groove_depth, centered=True)
left_groove = left_groove.translate((0, -oil_groove_position_y, 15 - oil_groove_depth / 2))
part = part.cut(left_groove)

# Right oil groove
right_groove = cq.Workplane("XZ").box(150, oil_groove_width, oil_groove_depth, centered=True)
right_groove = right_groove.translate((0, oil_groove_position_y, 15 - oil_groove_depth / 2))
part = part.cut(right_groove)

result = part
