import cadquery as cq
import math

# Create the main base block (150mm length, 100mm width, 30mm height)
base = cq.Workplane("XY").box(150, 100, 30, centered=True)

# Add the dovetail guide rail on top
# The dovetail is a trapezoidal protrusion with bottom width 60mm, height 15mm, side angles 60 degrees
height_dovetail = 15
bottom_width_dovetail = 60
angle_rad = math.radians(60)
offset = height_dovetail / math.tan(angle_rad)
top_width_dovetail = bottom_width_dovetail + 2 * offset

# Create the dovetail trapezoid in YZ plane, extruded along X (length direction)
dovetail_face = (
    cq.Workplane("YZ")
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

# Add T-slots on both sides (150x30 surfaces - the ends along X axis)
# T-slot: mouth width 10mm, internal width 16mm
t_slot_depth = 10
t_slot_mouth = 10
t_slot_internal = 16

# T-slot profile in XZ plane
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

# Create T-slot cuts (extrude profile along Y direction, on both sides)
t_slot_cut = t_slot_profile.extrude(100)
t_slot_cut_front = t_slot_cut.translate((0, -50, -10))
t_slot_cut_back = t_slot_cut.translate((0, 50, -10))

# Remove T-slots from part
part = part.cut(t_slot_cut_front)
part = part.cut(t_slot_cut_back)

# Add central countersunk hole on dovetail top surface
# Larger hole (countersink): diameter 40mm, depth 5mm
# Smaller hole (main): diameter 30mm
countersink = cq.Workplane("XY").cylinder(5, 20, centered=True).translate((0, 0, 30))
part = part.cut(countersink)

# Main hole through: 30mm diameter
main_hole = cq.Workplane("XY").cylinder(50, 15, centered=True).translate((0, 0, 0))
part = part.cut(main_hole)

# Add four corner mounting holes (8mm diameter)
corner_positions = [
    (-75, -50),
    (75, -50),
    (-75, 50),
    (75, 50),
]

for x, y in corner_positions:
    # Hole: 8mm diameter
    corner_hole = cq.Workplane("XY").cylinder(30, 4, centered=True).translate((x, y, -15))
    part = part.cut(corner_hole)

# Add oil groove relief at the root of dovetail (2mm wide, 1mm deep on both sides)
oil_groove_width = 2
oil_groove_depth = 1
oil_groove_position_y = (bottom_width_dovetail / 2)

# Left oil groove (in Y direction)
left_groove = cq.Workplane("XY").box(150, oil_groove_width, oil_groove_depth, centered=True)
left_groove = left_groove.translate((0, -oil_groove_position_y, 15 - oil_groove_depth / 2))
part = part.cut(left_groove)

# Right oil groove (in Y direction)
right_groove = cq.Workplane("XY").box(150, oil_groove_width, oil_groove_depth, centered=True)
right_groove = right_groove.translate((0, oil_groove_position_y, 15 - oil_groove_depth / 2))
part = part.cut(right_groove)

result = part
