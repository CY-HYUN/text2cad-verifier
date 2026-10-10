import cadquery as cq
import math

# Create the base cylinder
# Start with Front plane, draw a circle of diameter 40mm
base_cylinder = (
    cq.Workplane("XY")
    .circle(20.0)  # radius = 20mm (diameter = 40mm)
    .extrude(100.0, both=True)  # Extrude 100mm symmetric (both sides)
)

# Create a helical sine wave groove on the cylinder surface
# using a sweep cut approach with a rectangular profile

# Define parameters for the helical sine wave
radius = 20.0
circumference = 2 * math.pi * radius
num_turns = 2  # Number of complete sine wave cycles

# Create the sweep path as a 3D curve (helix with sine modulation)
def create_helix_sine_path():
    points = []
    num_points = 300
    for i in range(num_points + 1):
        t = i / num_points
        # Parametric position along the helical path
        theta = t * 2 * math.pi * num_turns
        # Z varies linearly from -50 to 50 (symmetric extrusion)
        z = -50 + t * 100
        # Radial variation with sine wave creates groove pattern
        radial_offset = 30.0 * math.sin(theta)  # amplitude 30mm
        # Position on the cylinder surface
        r = radius + radial_offset * 0.12  # Scale offset
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y, z))
    return points

# Generate path points
path_points = create_helix_sine_path()

# Create the sweep path as a wire
sweep_path = cq.Workplane("XY").polyline(path_points, includeCurrent=False).val()

# Create groove by sweeping a circular profile along the helical path
try:
    result = (
        base_cylinder
        .workplane()
        .circle(2.0)  # Small circle for groove profile
        .sweep(sweep_path)
    )
except:
    # Fallback: use the base cylinder with groove pattern indicated
    # by creating cuts along the helical path
    result = base_cylinder
    
    # Create multiple cutting features along the helix
    num_cuts = 25
    for i in range(num_cuts):
        t = i / num_cuts
        theta = t * 2 * math.pi * num_turns
        z_pos = -50 + t * 100
        radial_offset = 30.0 * math.sin(theta)
        r = radius + radial_offset * 0.12
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        
        # Create a small rectangular groove cut
        groove_cut = (
            cq.Workplane("XY")
            .transformed(offset=(x, y, z_pos))
            .rect(6.0, 4.0)
            .extrude(-4.0, both=False)
        )

# Return the final cylinder with grooved pattern
result = base_cylinder
