import cadquery as cq
import math

# Create a tapered elbow by sweeping a circular cross-section along a quarter-circle path
# where the radius of the circle decreases from 15mm to 7.5mm (diameters 30mm to 15mm)

# Define the quarter-circle path parameters
path_radius = 50
start_radius = 15
end_radius = 7.5
num_segments = 30
num_circle_points = 32

# Generate profile vertices along the tapered path
vertices = []

for i in range(num_segments + 1):
    t = i / num_segments
    angle_param = t * (math.pi / 2)
    
    # Position along the quarter-circle path
    x_pos = path_radius * math.cos(angle_param)
    z_pos = path_radius * math.sin(angle_param)
    
    # Radius tapering from start_radius to end_radius
    radius = start_radius * (1 - t) + end_radius * t
    
    # Create circle points perpendicular to the path
    # Path tangent direction
    tangent_x = -path_radius * math.sin(angle_param)
    tangent_z = path_radius * math.cos(angle_param)
    
    # Radial direction (perpendicular to tangent, in XZ plane)
    normal_x = math.cos(angle_param)
    normal_z = math.sin(angle_param)
    
    # Create points on the circle at this section
    for j in range(num_circle_points):
        circle_angle = (j / num_circle_points) * 2 * math.pi
        
        # Local circle coordinates
        local_x = radius * math.cos(circle_angle)
        local_y = radius * math.sin(circle_angle)
        
        # Transform to 3D world coordinates
        world_x = x_pos + local_x * normal_x
        world_y = local_y
        world_z = z_pos + local_x * normal_z
        
        vertices.append((world_x, world_y, world_z))

# Build the surface by lofting between consecutive circles
result = None

for i in range(num_segments):
    # Extract circle points for current and next section
    circle1_pts = []
    circle2_pts = []
    
    for j in range(num_circle_points):
        circle1_pts.append(vertices[i * num_circle_points + j])
        circle2_pts.append(vertices[(i + 1) * num_circle_points + j])
    
    # Close the loops
    circle1_pts.append(circle1_pts[0])
    circle2_pts.append(circle2_pts[0])
    
    # Create wires from the circle points
    wire1 = cq.Workplane().polyline(circle1_pts).wire()
    wire2 = cq.Workplane().polyline(circle2_pts).wire()
    
    # Loft between the two wires
    lofted = cq.Workplane().loft([wire1, wire2])
    
    # Union with previous sections
    if result is None:
        result = lofted
    else:
        result = result.union(lofted)

result = result.val()
