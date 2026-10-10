import cadquery as cq
import math

# Create a wavy vase with lofting between circular and sinusoidal cross-sections

def create_circle_profile(radius, z_height):
    """Create a circular profile at given height"""
    points = []
    steps = 64
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y, z_height))
    points.append(points[0])  # Close the loop
    return points

def create_sinusoidal_profile(avg_radius, amplitude, num_peaks, z_height, rotation=0):
    """Create a sinusoidal ring profile with peaks"""
    points = []
    steps = 256  # High resolution for smooth waves
    for i in range(steps):
        angle = 2 * math.pi * i / steps + rotation
        # Sinusoidal variation in radius
        radius = avg_radius + amplitude * math.sin(num_peaks * angle)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y, z_height))
    points.append(points[0])  # Close the loop
    return points

# Parameters
base_radius = 30  # diameter 60mm
top_radius = 40   # diameter 80mm
height = 150
mid_height = 75
avg_mid_radius = 35  # average diameter 70mm
wave_amplitude = 5
num_peaks = 6
rotation = 0  # One peak aligned with positive X-axis

# Create profiles at different heights
profile_bottom = create_circle_profile(base_radius, 0)
profile_mid = create_sinusoidal_profile(avg_mid_radius, wave_amplitude, num_peaks, mid_height, rotation)
profile_top = create_circle_profile(top_radius, height)

# Create intermediate profiles for smooth lofting
profile_quarter = create_circle_profile(base_radius + (avg_mid_radius - base_radius) * 0.5, mid_height * 0.5)
profile_three_quarter = create_circle_profile(avg_mid_radius + (top_radius - avg_mid_radius) * 0.5, mid_height + (height - mid_height) * 0.5)

# Start with base profile
workplane = cq.Workplane("XY")

# Create wires for each profile
wire_bottom = cq.Wire.makePolygon([(p[0], p[1]) for p in profile_bottom])
wire_quarter = cq.Wire.makePolygon([(p[0], p[1]) for p in profile_quarter])
wire_mid = cq.Wire.makePolygon([(p[0], p[1]) for p in profile_mid])
wire_three_quarter = cq.Wire.makePolygon([(p[0], p[1]) for p in profile_three_quarter])
wire_top = cq.Wire.makePolygon([(p[0], p[1]) for p in profile_top])

# Create faces at each level by revolving/lofting
# Use loft to create smooth transitions between profiles

# Create edges at each height for lofting
edge_bottom = wire_bottom.Edge(0)
edge_quarter = wire_quarter.Edge(0)
edge_mid = wire_mid.Edge(0)
edge_three_quarter = wire_three_quarter.Edge(0)
edge_top = wire_top.Edge(0)

# Create a face for each section and loft between them
shell_bottom = cq.Shell.makeLoft([wire_bottom, wire_quarter])
shell_mid = cq.Shell.makeLoft([wire_quarter, wire_mid])
shell_mid_upper = cq.Shell.makeLoft([wire_mid, wire_three_quarter])
shell_top = cq.Shell.makeLoft([wire_three_quarter, wire_top])

# Combine all shells into a single compound
shells = [shell_bottom, shell_mid, shell_mid_upper, shell_top]
result = cq.Compound.makeCompound(shells)

# Convert to solid by sewing
try:
    result = cq.Solid.makeSolid(cq.Shell.makeShell(shells))
except:
    # If sewing fails, keep as compound
    result = cq.Compound.makeCompound(shells)
