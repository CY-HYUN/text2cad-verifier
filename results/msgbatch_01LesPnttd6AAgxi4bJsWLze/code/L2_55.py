import cadquery as cq
import math

# Create a tapered elbow by sweeping a circular cross-section along a quarter-circle path
# where the radius of the circle decreases from 15mm to 7.5mm (diameters 30mm to 15mm)

# Define the quarter-circle path (90-degree elbow with 50mm radius)
path_points = []
num_segments = 50
for i in range(num_segments + 1):
    angle = (i / num_segments) * (math.pi / 2)  # 0 to 90 degrees
    x = 50 * math.cos(angle)
    y = 0
    z = 50 * math.sin(angle)
    path_points.append((x, y, z))

# Create the path as a wire
path_wire = cq.Workplane().polyline(path_points).wire()

# Create cross-sections that taper from 15mm radius to 7.5mm radius
# We'll create multiple circles along the path and sweep
profiles = []
for i in range(num_segments + 1):
    # Interpolate radius from 15mm to 7.5mm
    t = i / num_segments
    radius = 15 * (1 - t) + 7.5 * t
    
    # Get the position along the path
    angle = t * (math.pi / 2)
    x = 50 * math.cos(angle)
    z = 50 * math.sin(angle)
    
    # Create a circle at this position
    # The circle should be perpendicular to the path direction
    # Path direction: tangent to circle, pointing in direction of increasing angle
    tangent_x = -50 * math.sin(angle)
    tangent_z = 50 * math.cos(angle)
    
    # Create a circle in the plane perpendicular to the tangent
    circle = cq.Workplane("XY").circle(radius)
    
    # Position and rotate the circle to be perpendicular to the path
    profiles.append({
        'pos': (x, 0, z),
        'radius': radius,
        'tangent': (tangent_x, 0, tangent_z),
        'angle': angle
    })

# Create the swept surface using a series of circular cross-sections
# Build using successive circular sections positioned along the path
vertices = []
num_circle_points = 32

for i in range(len(profiles)):
    profile = profiles[i]
    x_pos = profile['pos'][0]
    z_pos = profile['pos'][2]
    radius = profile['radius']
    angle_param = profile['angle']
    
    # Create circle points in local XY plane, then transform
    for j in range(num_circle_points):
        circle_angle = (j / num_circle_points) * 2 * math.pi
        
        # Local circle coordinates
        local_x = radius * math.cos(circle_angle)
        local_y = radius * math.sin(circle_angle)
        
        # The circle is perpendicular to the path direction
        # Path is in XZ plane curving from (50,0,0) to (0,0,50)
        # At each point, rotate the circle normal to be perpendicular to tangent
        
        # Tangent direction
        tangent_x = -50 * math.sin(angle_param)
        tangent_z = 50 * math.cos(angle_param)
        
        # Create perpendicular vectors
        # Normal to path (radial): points outward from center
        normal_x = math.cos(angle_param)
        normal_z = math.sin(angle_param)
        
        # Binormal: Y direction (perpendicular to both path and normal in path plane)
        binormal_y = 1.0
        
        # Transform local circle to 3D
        world_x = x_pos + local_x * normal_x + local_y * 0
        world_y = 0 + local_x * 0 + local_y * binormal_y
        world_z = z_pos + local_x * normal_z + local_y * 0
        
        vertices.append((world_x, world_y, world_z))

# Create faces by connecting the circular sections
faces = []
for i in range(len(profiles) - 1):
    for j in range(num_circle_points):
        j_next = (j + 1) % num_circle_points
        
        # Four corners of the quad
        p1_idx = i * num_circle_points + j
        p2_idx = i * num_circle_points + j_next
        p3_idx = (i + 1) * num_circle_points + j_next
        p4_idx = (i + 1) * num_circle_points + j
        
        faces.append([p1_idx, p2_idx, p3_idx, p4_idx])

# Build the shape from vertices and faces
builder = cq.Workplane().makePolygon(vertices)

# Create shell by manually constructing the surface
# Use loft between consecutive circles
result = None
for i in range(len(profiles) - 1):
    circle1_pts = []
    circle2_pts = []
    
    for j in range(num_circle_points + 1):
        j_idx = j % num_circle_points
        circle1_pts.append(vertices[i * num_circle_points + j_idx])
        circle2_pts.append(vertices[(i + 1) * num_circle_points + j_idx])
    
    wire1 = cq.Workplane().polyline(circle1_pts).wire()
    wire2 = cq.Workplane().polyline(circle2_pts).wire()
    
    lofted = cq.Workplane().loft([wire1, wire2])
    
    if result is None:
        result = lofted
    else:
        result = result.union(lofted)

result = result.val()
