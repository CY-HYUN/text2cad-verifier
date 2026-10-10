import cadquery as cq
import math

# Start with the base rectangular block
base = cq.Workplane("XY").box(150, 100, 30, centered=True)

# The base top is at Z=30, bottom at Z=0, centered at origin in XY

# Create the dovetail guide on top of the base
# Dovetail is a trapezoid in YZ plane, centered on top of base
# Lower base (at Z=30): 60 mm wide in Y
# Upper base (at Z=45): 42.68 mm wide in Y
# Height: 15 mm

# Calculate the offset for the slanted sides
# tan(30°) = 1/√3 ≈ 0.5773
# offset = 15 * tan(30°) ≈ 8.66 mm
offset = 15 * math.tan(math.radians(30))

# Create dovetail trapezoid profile
dovetail_profile = (
    cq.Workplane("YZ")
    .moveTo(-30, 30)  # Bottom left at Z=30, Y=-30 (half of 60)
    .lineTo(30, 30)   # Bottom right at Z=30, Y=30
    .lineTo(30 - offset, 45)  # Top right at Z=45
    .lineTo(-30 + offset, 45)  # Top left at Z=45
    .close()
    .extrude(150, both=False)  # Extrude along X-axis (150 mm)
)

# Move dovetail to correct position (centered in X, starting at Z=30)
dovetail_profile = dovetail_profile.translate((0, 0, 0))

# Combine base with dovetail
part = base.union(dovetail_profile)

# Cut oil grooves on both sides of dovetail at Z=30
# Left groove at Y = -30 - 2/2 = -31 (offset by groove width/2)
# Right groove at Y = 30 + 2/2 = 31
# Each groove: 2mm wide (Y), 1mm deep (Z), 150mm long (X)

groove_left = (
    cq.Workplane("XY")
    .box(150, 2, 1, centered=True)
    .translate((0, -31, 29.5))  # Center at Y=-31, Z=29.5 (bottom at Z=29)
)

groove_right = (
    cq.Workplane("XY")
    .box(150, 2, 1, centered=True)
    .translate((0, 31, 29.5))  # Center at Y=31, Z=29.5
)

part = part.cut(groove_left).cut(groove_right)

# Cut side T-slots on Y = +50 and Y = -50 surfaces
# T-slot centerline at Z = 15 mm
# Opening: 10mm wide (X), 6mm deep (into the base)
# Widened part below: 16mm wide (X), 6mm deep
# Total cutting depth: 12mm

# Left T-slot (Y = -50)
t_slot_opening_left = (
    cq.Workplane("XZ")
    .box(10, 6, 150, centered=True)
    .translate((0, -50 + 3, 15))  # 3mm inward from surface
)

t_slot_wide_left = (
    cq.Workplane("XZ")
    .box(16, 6, 150, centered=True)
    .translate((0, -50 + 9, 15 - 6))  # 6mm below opening
)

# Right T-slot (Y = +50)
t_slot_opening_right = (
    cq.Workplane("XZ")
    .box(10, 6, 150, centered=True)
    .translate((0, 50 - 3, 15))
)

t_slot_wide_right = (
    cq.Workplane("XZ")
    .box(16, 6, 150, centered=True)
    .translate((0, 50 - 9, 15 - 6))
)

part = part.cut(t_slot_opening_left).cut(t_slot_wide_left)
part = part.cut(t_slot_opening_right).cut(t_slot_wide_right)

# Cut central through-hole
# Diameter: 30mm, from Z=45 through to Z=0
through_hole = (
    cq.Workplane("XY")
    .circle(15)  # radius 15mm
    .extrude(-45, both=False)  # extrude down 45mm
    .translate((0, 0, 45))
)

part = part.cut(through_hole)

# Cut counterbore on top surface
# Diameter: 40mm, depth: 5mm, bottom at Z=40
counterbore = (
    cq.Workplane("XY")
    .circle(20)  # radius 20mm
    .extrude(-5, both=False)  # 5mm deep
    .translate((0, 0, 45))
)

part = part.cut(counterbore)

result = part
