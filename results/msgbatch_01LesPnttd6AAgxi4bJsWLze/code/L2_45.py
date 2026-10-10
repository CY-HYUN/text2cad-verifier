import cadquery as cq
import math

# Parameters
total_length = 100
avg_diameter = 40
wall_thickness = 2
peak_diameter = 45
trough_diameter = 35
wavelength = 10
num_cycles = 10
straight_section_length = 5

# Calculate radii
peak_radius = peak_diameter / 2
trough_radius = trough_diameter / 2
avg_radius = avg_diameter / 2
inner_peak_radius = peak_radius - wall_thickness
inner_trough_radius = trough_radius - wall_thickness

# Wavy length
wavy_length = num_cycles * wavelength
straight_total = 2 * straight_section_length

# Create points for the outer profile
outer_points = []
inner_points = []

# Front straight section
for z in [0, straight_section_length]:
    outer_points.append((avg_radius, z))
    inner_points.append((avg_radius - wall_thickness, z))

# Wavy section
num_points = num_cycles * 20 + 1
for i in range(num_points):
    z = straight_section_length + (i / (num_points - 1)) * wavy_length
    # Sine wave: oscillates between peak and trough
    phase = (z - straight_section_length) / wavelength * 2 * math.pi
    outer_r = avg_radius + (peak_radius - avg_radius) * math.sin(phase)
    inner_r = outer_r - wall_thickness
    outer_points.append((outer_r, z))
    inner_points.append((inner_r, z))

# Rear straight section
for z in [straight_section_length + wavy_length, straight_section_length + wavy_length + straight_section_length]:
    outer_points.append((avg_radius, z))
    inner_points.append((avg_radius - wall_thickness, z))

# Remove duplicates that may occur at boundaries
outer_points_clean = []
inner_points_clean = []
for i, pt in enumerate(outer_points):
    if i == 0 or pt != outer_points[i-1]:
        outer_points_clean.append(pt)
        inner_points_clean.append(inner_points[i])

outer_points = outer_points_clean
inner_points = inner_points_clean

# Create outer profile wire (revolve around z-axis)
outer_profile = cq.Workplane("XZ").polyline(outer_points).close()

# Revolve outer profile to create outer surface
outer_solid = outer_profile.revolve(axis=(0, 0, 1), angleDegrees=360)

# Create inner profile
inner_profile = cq.Workplane("XZ").polyline(inner_points).close()

# Revolve inner profile to create inner cavity
inner_solid = inner_profile.revolve(axis=(0, 0, 1), angleDegrees=360)

# Create the bellows by subtracting inner from outer
result = outer_solid.cut(inner_solid)
