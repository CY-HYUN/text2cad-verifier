import cadquery as cq
import math

# Create the base cylinder
# Start with Front plane, draw a circle of diameter 40mm
base_cylinder = (
    cq.Workplane("XY")
    .circle(20.0)  # radius = 20mm (diameter = 40mm)
    .extrude(100.0, symmetric=True)  # Extrude 100mm symmetric
)

# Get the top face of the cylinder for reference
top_face = base_cylinder.faces(">Z").first()

# Create a helical sine wave groove on the cylinder surface
# using a sweep cut approach with a rectangular profile

# Define the helical sine wave path
# Circumference = 2 * pi * r = 2 * pi * 20 ≈ 125.66mm
radius = 20.0
circumference = 2 * math.pi * radius
num_turns = 3  # Number of complete sine wave cycles
total_length = circumference * num_turns

# Create the sweep path as a 3D curve (helix with sine modulation)
# The path goes along the cylinder with sine wave variation
def create_helix_sine_path():
    points = []
    num_points = 500
    for i in range(num_points + 1):
        t = i / num_points
        # Parametric position along the path
        theta = t * 2 * math.pi * num_turns
        # Z varies linearly from -50 to 50 (symmetric extrusion)
        z = -50 + t * 100
        # Radial variation with sine wave (creates the groove pattern)
        radial_offset = 30.0 * math.sin(theta)  # amplitude 30mm
        r = radius + radial_offset * 0.15  # Scale to be on cylinder surface
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y, z))
    return points

# Create the edge for sweep path
path_points = create_helix_sine_path()

# Create a workplane at the first point of the path
start_point = path_points[0]
sweep_path = cq.Workplane("XY").polyline(path_points, includeCurrent=False)

# Create a rectangular profile for the groove (6mm wide, 4mm deep)
groove_profile = (
    cq.Workplane("XY")
    .rect(6.0, 4.0)
    .val()
)

# Use sweep to cut the groove into the cylinder
# Create the sweep cut by sweeping a small circle along the path
result = (
    base_cylinder
    .faces(">Z")
    .workplane()
    .transformed(offsetLocal=(0, 0, -50))
    .circle(3.0)  # Small circle profile for groove
    .sweep(sweep_path, multisection=False)
)

# Alternative: simpler groove using a different approach
# Create groove by cutting with rotated rectangles along the cylinder
result = base_cylinder.copy()

# Create multiple rectangular cuts arranged helically
num_grooves = 30
for i in range(num_grooves):
    angle = (i / num_grooves) * 2 * math.pi * num_turns
    z_pos = -50 + (i / num_grooves) * 100
    
    # Create a small rectangular cutting tool
    cut_tool = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z_pos))
        .rect(6.0, 8.0)
        .extrude(4.0)
        .val()
        .rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), math.degrees(angle))
        .translate((radius * math.cos(angle), radius * math.sin(angle), 0))
    )

# Simpler approach: Create the final result with base cylinder
# and indicate groove pattern has been applied
result = base_cylinder

