import cadquery as cq
import math

# Create the parabolic reflector focusing cup

# Step 1: Create the main shell with parabolic inner surface
# Z = R^2/80, where height is 80mm and R ranges from 0 to 80mm at the top

# Create a solid by revolving a closed profile
shell_profile_points = []

# Inner surface (parabola)
for r in range(0, 81, 2):
    z = (r * r) / 80.0
    shell_profile_points.append((r, z))

# Outer surface (offset parabola by 5mm normal)
for r in range(80, -1, -2):
    z = (r * r) / 80.0
    slope = r / 40.0 if r > 0 else 0
    normal_len = math.sqrt(slope * slope + 1)
    normal_x = -slope / normal_len
    normal_z = 1 / normal_len
    
    outer_r = r + 5.0 * normal_x
    outer_z = z + 5.0 * normal_z
    shell_profile_points.append((outer_r, outer_z))

# Create the main shell by revolving
shell = cq.Workplane("XZ").polyline(shell_profile_points).close().revolve(360, (0, 0, 0), (0, 0, 1))

# Step 2: Add the flange at the top
# Flange: outer radius 95mm, inner radius 85mm, thickness 5mm
flange = (cq.Workplane("XY")
    .circle(95)
    .extrude(5)
    .faces(">Z")
    .circle(85)
    .cutThruAll())

# Combine shell and flange
result = shell.union(flange)

# Step 3: Add mounting holes (4 holes at radius 90mm, diameter 5mm)
hole_radius = 90
hole_diameter = 5

for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = hole_radius * math.cos(rad)
    y = hole_radius * math.sin(rad)
    hole = (cq.Workplane("XY")
        .moveTo(x, y)
        .circle(hole_diameter / 2)
        .extrude(-10))
    result = result.cut(hole)

# Step 4: Cut the light source hole at the center bottom (diameter 10mm)
center_hole = (cq.Workplane("XY")
    .circle(5)
    .extrude(-100))
result = result.cut(center_hole)
