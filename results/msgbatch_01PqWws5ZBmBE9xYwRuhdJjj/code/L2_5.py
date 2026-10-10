import cadquery as cq
import math

# Create a sketch for the main path and branches
def create_path_sketch():
    """Create a 3D path that branches into two arms at 60 degrees"""
    # Main vertical path: from origin to branch point
    main_height = 60
    branch_height = 40
    
    # We'll create the path using points
    # Start at origin, go up the main stem, then branch into two paths
    points = []
    
    # Main stem going up
    points.append((0, 0, 0))
    points.append((0, 0, main_height))
    
    # Branch point
    branch_point = (0, 0, main_height)
    
    # Two branches at 60 degrees apart
    angle1 = math.radians(30)  # 30 degrees from vertical
    angle2 = math.radians(-30)  # -30 degrees from vertical
    
    # Branch 1
    branch1_end_x = branch_height * math.sin(angle1)
    branch1_end_z = branch_height * math.cos(angle1)
    points_branch1 = [
        (0, 0, main_height),
        (branch1_end_x, 0, main_height + branch1_end_z)
    ]
    
    # Branch 2
    branch2_end_x = branch_height * math.sin(angle2)
    branch2_end_z = branch_height * math.cos(angle2)
    points_branch2 = [
        (0, 0, main_height),
        (branch2_end_x, 0, main_height + branch2_end_z)
    ]
    
    return points, points_branch1, points_branch2

# Create the Y-shaped pipe using sweep operations
points, branch1_pts, branch2_pts = create_path_sketch()

# Create circular profile (20mm diameter = 10mm radius)
profile_radius = 10

# Create the main stem pipe
plane_bottom = cq.Workplane("XY").workplane(offset=0)
profile_main = plane_bottom.circle(profile_radius)

# Sweep along main stem
main_stem = profile_main.sweep(
    cq.Workplane("XY").polyline(points).val(),
    makeSolid=False
)

# Create branch 1 pipe
profile_branch1 = cq.Workplane("XY").circle(profile_radius)
branch1_swept = profile_branch1.sweep(
    cq.Workplane("XY").polyline(branch1_pts).val(),
    makeSolid=False
)

# Create branch 2 pipe
profile_branch2 = cq.Workplane("XY").circle(profile_radius)
branch2_swept = profile_branch2.sweep(
    cq.Workplane("XY").polyline(branch2_pts).val(),
    makeSolid=False
)

# Create solids from the swept profiles
main_stem_solid = cq.Workplane("XY").circle(profile_radius).sweep(
    cq.Workplane("XY").polyline(points).val(),
    makeSolid=True
)

branch1_solid = cq.Workplane("XY").circle(profile_radius).sweep(
    cq.Workplane("XY").polyline(branch1_pts).val(),
    makeSolid=True
)

branch2_solid = cq.Workplane("XY").circle(profile_radius).sweep(
    cq.Workplane("XY").polyline(branch2_pts).val(),
    makeSolid=True
)

# Union the three parts to create the Y-shaped solid
y_shaped = main_stem_solid.union(branch1_solid).union(branch2_solid)

# Apply shell operation to create a hollow pipe with uniform wall thickness
wall_thickness = 2
result = y_shaped.shell(wall_thickness)

# Remove the three end faces by selecting and deleting them
# Get all faces and remove the ones at the ends
faces_to_remove = result.faces("+Z or -Z or +X").val()

# Create the final hollow Y-shaped pipe
# We need to remove the end caps
result = y_shaped.shell(wall_thickness)

