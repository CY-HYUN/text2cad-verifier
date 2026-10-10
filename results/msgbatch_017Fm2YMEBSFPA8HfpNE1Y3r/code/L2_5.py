import cadquery as cq
import math

# Create a proper Y-shaped pipe using sweep with circles at key points
profile_radius = 10
wall_thickness = 2

# Main stem parameters
main_height = 60
branch_length = 40

# Create path points for main stem
main_path = [
    (0, 0, 0),
    (0, 0, main_height)
]

# Branch angles (30 degrees from vertical in XZ plane)
angle = math.radians(30)
branch1_end_x = branch_length * math.sin(angle)
branch1_end_z = branch_length * math.cos(angle)
branch2_end_x = -branch_length * math.sin(angle)
branch2_end_z = branch_length * math.cos(angle)

# Create path points for branches
branch1_path = [
    (0, 0, main_height),
    (branch1_end_x, 0, main_height + branch1_end_z)
]

branch2_path = [
    (0, 0, main_height),
    (branch2_end_x, 0, main_height + branch2_end_z)
]

# Create wire paths for sweeping
main_wire = cq.Workplane("XY").polyline(main_path).val()
branch1_wire = cq.Workplane("XY").polyline(branch1_path).val()
branch2_wire = cq.Workplane("XY").polyline(branch2_path).val()

# Create circular profile
profile = cq.Workplane("XY").circle(profile_radius)

# Sweep main stem
main_stem = profile.sweep(main_wire, makeSolid=True)

# Sweep branch 1
branch1 = profile.sweep(branch1_wire, makeSolid=True)

# Sweep branch 2
branch2 = profile.sweep(branch2_wire, makeSolid=True)

# Union all three parts together
y_shape_solid = main_stem.union(branch1).union(branch2)

# Shell to create hollow pipe
result = y_shape_solid.shell(wall_thickness)

