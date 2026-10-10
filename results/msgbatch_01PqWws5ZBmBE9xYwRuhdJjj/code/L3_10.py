import cadquery as cq
import math

# Create the parabolic reflector focusing cup

# Step 1: Create the parabolic inner surface profile
# Z = R^2/80, where height is 80mm and R ranges from 0 to 80mm at the top
# We'll create a 2D profile that will be revolved

# Generate parabolic profile points
profile_points = []
for r in range(0, 81, 2):
    z = (r * r) / 80.0
    profile_points.append((r, z))

# Create the profile as a wire (open spline)
profile = cq.Workplane("XZ").spline(profile_points, includeCurrent=False)

# Step 2: Revolve the profile around Z-axis to create the inner parabolic surface
inner_surface = profile.revolve(360, (0, 0, 0), (0, 0, 1))

# Step 3: Create the outer surface by offsetting the inner surface outward by 5mm
# We need to create points for the outer surface at radius + 5mm thickness
outer_profile_points = []
for r in range(0, 81, 2):
    z = (r * r) / 80.0
    # Calculate the slope to determine the normal direction for offset
    # dz/dr = 2r/80 = r/40
    slope = r / 40.0
    # Normal offset perpendicular to the surface
    offset_dist = 5.0
    # Normal vector components: (-slope, 0, 1) normalized
    normal_len = math.sqrt(slope * slope + 1)
    normal_x = -slope / normal_len
    normal_z = 1 / normal_len
    
    outer_r = r + offset_dist * normal_x
    outer_z = z + offset_dist * normal_z
    outer_profile_points.append((outer_r, outer_z))

# Create outer profile
outer_profile = cq.Workplane("XZ").spline(outer_profile_points, includeCurrent=False)

# Revolve to create outer surface
outer_surface = outer_profile.revolve(360, (0, 0, 0), (0, 0, 1))

# Step 4: Create the main shell by lofting between inner and outer surfaces
# Create a solid cup by using a revolved profile that includes both surfaces
shell_profile_points = []
for r in range(0, 81, 2):
    z = (r * r) / 80.0
    slope = r / 40.0
    normal_len = math.sqrt(slope * slope + 1)
    normal_x = -slope / normal_len
    normal_z = 1 / normal_len
    
    outer_r = r + 5.0 * normal_x
    outer_z = z + 5.0 * normal_z
    shell_profile_points.append((r, z))

# Create a closed profile for the shell (from center to outer edge, then back)
closed_profile = []
for r in range(0, 81, 2):
    z = (r * r) / 80.0
    closed_profile.append((r, z))

for r in range(80, -1, -2):
    z = (r * r) / 80.0
    slope = r / 40.0
    normal_len = math.sqrt(slope * slope + 1)
    normal_x = -slope / normal_len
    normal_z = 1 / normal_len
    
    outer_r = r + 5.0 * normal_x
    outer_z = z + 5.0 * normal_z
    closed_profile.append((outer_r, outer_z))

# Create shell by revolving the thickness profile
shell = cq.Workplane("XZ").spline(closed_profile, includeCurrent=False).revolve(360, (0, 0, 0), (0, 0, 1))

# Step 5: Add the flange at the top
# The flange extends from radius 85mm to 95mm at the top
# Flange thickness is 5mm and sits flush with cup opening (at z=0)

# Create flange as a separate cylinder-like feature
flange = cq.Workplane("XY").rect(190, 190).circle(95).extrude(5)
flange = flange.cut(cq.Workplane("XY").circle(85).extrude(10))

# Step 6: Add mounting holes (4 holes, uniformly distributed on flange at radius 90mm)
# One hole at positive Y direction
angles = [0, 90, 180, 270]  # degrees
hole_radius = 90
hole_diameter = 5

for angle in angles:
    rad = math.radians(angle)
    x = hole_radius * math.cos(rad)
    y = hole_radius * math.sin(rad)
    # Create hole from top through flange
    hole = cq.Workplane("XY").workplane(offset=5).circle(hole_diameter/2).hole(10)
    
# Use a more direct approach - create holes with pattern
base = shell.union(flange)

# Create 4 mounting holes
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = hole_radius * math.cos(rad)
    y = hole_radius * math.sin(rad)
    hole_cut = cq.Workplane("XY").moveTo(x, y).circle(hole_diameter/2).extrude(-10)
    base = base.cut(hole_cut)

# Step 7: Cut the light source hole at the center bottom (diameter 10mm)
center_hole = cq.Workplane("XY").circle(5).extrude(-100)
result = base.cut(center_hole)
