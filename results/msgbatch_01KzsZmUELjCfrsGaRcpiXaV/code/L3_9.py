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
        points.append((x, y))
    return points

def create_sinusoidal_profile(avg_radius, amplitude, num_peaks, rotation=0):
    """Create a sinusoidal ring profile with peaks"""
    points = []
    steps = 256  # High resolution for smooth waves
    for i in range(steps):
        angle = 2 * math.pi * i / steps + rotation
        # Sinusoidal variation in radius
        radius = avg_radius + amplitude * math.sin(num_peaks * angle)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
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

# Create 2D profiles
profile_bottom = create_circle_profile(base_radius, 0)
profile_quarter = create_circle_profile(base_radius + (avg_mid_radius - base_radius) * 0.5, mid_height * 0.5)
profile_mid = create_sinusoidal_profile(avg_mid_radius, wave_amplitude, num_peaks, rotation)
profile_three_quarter = create_circle_profile(avg_mid_radius + (top_radius - avg_mid_radius) * 0.5, mid_height + (height - mid_height) * 0.5)
profile_top = create_circle_profile(top_radius, height)

# Create wires for lofting
wire_bottom = cq.Wire.makePolygon(profile_bottom)
wire_quarter = cq.Wire.makePolygon(profile_quarter)
wire_mid = cq.Wire.makePolygon(profile_mid)
wire_three_quarter = cq.Wire.makePolygon(profile_three_quarter)
wire_top = cq.Wire.makePolygon(profile_top)

# Loft between consecutive profiles
shell_bottom = cq.Shell.makeLoft([wire_bottom, wire_quarter])
shell_mid_lower = cq.Shell.makeLoft([wire_quarter, wire_mid])
shell_mid_upper = cq.Shell.makeLoft([wire_mid, wire_three_quarter])
shell_top = cq.Shell.makeLoft([wire_three_quarter, wire_top])

# Combine all shells
shells = [shell_bottom, shell_mid_lower, shell_mid_upper, shell_top]

# Create a compound solid
result = cq.Compound.makeCompound(shells)

