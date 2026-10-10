import cadquery as cq
import math

# Define parameters
length = 100  # mm (along X-axis)
width = 50    # mm (along Y-axis)
base_thickness = 5  # mm
fin_height = 30  # mm
fin_thickness = 1  # mm
amplitude = 2  # mm
num_fins = 5

# Create the base (rectangular prism)
base = cq.Workplane("XY").box(length, width, base_thickness, centered=False)

# Create a single fin using a simpler approach with a sweep
def create_sine_fin(length, fin_height, fin_thickness, amplitude):
    """Create a corrugated fin by sweeping a rectangle along a sine path"""
    
    # Create the cross-section profile (rectangle in YZ plane)
    profile = cq.Workplane("YZ").rect(fin_thickness, fin_height)
    
    # Create the centerline path as a sine wave in XY plane
    # Sample points along the sine curve
    num_samples = 50
    path_points = []
    
    for i in range(num_samples + 1):
        x = i * length / num_samples
        y = amplitude * math.sin(0.2 * math.pi * x)
        path_points.append((x, y, base_thickness + fin_height / 2))
    
    # Create wire from path points
    path_wire = cq.Workplane("XYZ").polyline(path_points)
    
    # Sweep the profile along the path
    fin = profile.sweep(path_wire)
    
    return fin

# Create fins at different Y positions
fin_y_positions = [width / (num_fins + 1) * (i + 1) for i in range(num_fins)]

result = base

for y_pos in fin_y_positions:
    fin = create_sine_fin(length, fin_height, fin_thickness, amplitude)
    fin = fin.translate((0, y_pos, 0))
    result = result.union(fin)

