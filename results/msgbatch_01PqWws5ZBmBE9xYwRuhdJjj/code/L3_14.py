import cadquery as cq
import math

# Create the base rectangle on the XY plane
base = cq.Workplane("XY").rect(100, 50).extrude(5.0)

# Get the top surface of the base for the fin sketch
top_face = base.faces(">Z").first()

# Create the first fin using a sweep operation
# Define the sine curve path in 3D space
def sine_curve_path(num_points=100):
    points = []
    for i in range(num_points + 1):
        x = i * 100.0 / num_points
        y = 2 * math.sin(0.2 * math.pi * x)
        z = 5.0  # Start at the top of the base
        points.append((x - 50, y + 5.0, z))  # Center X, offset Y by 5mm from edge
    return points

# Create a profile for the fin (a small rectangle perpendicular to the path)
fin_profile = cq.Workplane("XY").rect(1.0, 30.0).val()

# Create the sine curve path
curve_points = sine_curve_path(100)

# Create a wire from the curve points for the sweep path
sweep_path = cq.Workplane("XY").polyline(curve_points).val()

# Perform the sweep operation to create the first fin
fin = cq.Workplane("XY").sweep(sweep_path, fin_profile, isFrenet=True)

# Combine base with the first fin
model = base.union(fin)

# Create a linear pattern of the fin along the Y-axis
# We need to create the fin feature multiple times at different Y positions
fins = base

# Create 5 instances of the fin with 10mm spacing along Y-axis
for i in range(5):
    offset_y = i * 10.0 - 20.0  # Center the pattern
    
    # Adjust the curve for this fin instance
    fin_points = []
    for j in range(101):
        x = j * 100.0 / 100
        y = 2 * math.sin(0.2 * math.pi * x)
        z = 5.0
        fin_points.append((x - 50, offset_y + y + 5.0, z))
    
    # Create sweep path
    fin_sweep_path = cq.Workplane("XY").polyline(fin_points).val()
    
    # Create fin profile
    fin_profile_2d = cq.Workplane("XY").rect(1.0, 30.0).val()
    
    # Perform sweep
    fin_instance = cq.Workplane("XY").sweep(fin_sweep_path, fin_profile_2d, isFrenet=True)
    
    # Union with the model
    fins = fins.union(fin_instance)

result = fins
