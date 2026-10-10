import cadquery as cq
import math

# Parameters
base_circle_radius = 3  # mm
involute_angle_max = 1080  # degrees (3 turns)
wall_thickness = 4  # mm
wall_height = 25  # mm
plate_diameter = 80  # mm
plate_thickness = 5  # mm

# Create the scroll plate (circular disk)
plate = cq.Workplane("XY").circle(plate_diameter / 2).extrude(plate_thickness)

# Function to generate involute curve points
def involute_point(angle_deg, base_radius):
    """Generate a point on an involute curve"""
    angle_rad = math.radians(angle_deg)
    # Involute parametric equations
    x = base_radius * (math.cos(angle_rad) + angle_rad * math.sin(angle_rad))
    y = base_radius * (math.sin(angle_rad) - angle_rad * math.cos(angle_rad))
    return (x, y)

# Generate involute centerline points
num_points = 180
involute_points_2d = []
for i in range(num_points + 1):
    angle = (i / num_points) * involute_angle_max
    point = involute_point(angle, base_circle_radius)
    involute_points_2d.append(point)

# Create inner and outer edges of the wall
inner_edge_points = []
outer_edge_points = []

for i in range(len(involute_points_2d)):
    angle = (i / num_points) * involute_angle_max
    angle_rad = math.radians(angle)
    x, y = involute_points_2d[i]
    
    # Tangent direction of involute
    tangent_x = -base_circle_radius * math.sin(angle_rad) + base_circle_radius * angle_rad * math.cos(angle_rad)
    tangent_y = base_circle_radius * math.cos(angle_rad) + base_circle_radius * angle_rad * math.sin(angle_rad)
    
    # Normalize tangent
    tangent_length = math.sqrt(tangent_x**2 + tangent_y**2)
    if tangent_length > 0.001:
        tangent_x /= tangent_length
        tangent_y /= tangent_length
    else:
        tangent_x, tangent_y = 1, 0
    
    # Normal direction (perpendicular to tangent, rotated 90 degrees)
    normal_x = -tangent_y
    normal_y = tangent_x
    
    # Inner and outer edges of the wall
    inner_x = x - (wall_thickness / 2) * normal_x
    inner_y = y - (wall_thickness / 2) * normal_y
    outer_x = x + (wall_thickness / 2) * normal_x
    outer_y = y + (wall_thickness / 2) * normal_y
    
    inner_edge_points.append((inner_x, inner_y))
    outer_edge_points.append((outer_x, outer_y))

# Create the scroll wall by lofting between inner and outer edges
# Build a solid scroll wall
wall_points_bottom = [(x, y, plate_thickness) for x, y in inner_edge_points]
wall_points_top = [(x, y, plate_thickness + wall_height) for x, y in inner_edge_points]
outer_points_bottom = [(x, y, plate_thickness) for x, y in outer_edge_points]
outer_points_top = [(x, y, plate_thickness + wall_height) for x, y in outer_edge_points]

# Create faces and combine
# Build the wall as two lofted surfaces (inner and outer) connected at ends
inner_loft_points = [wall_points_bottom, wall_points_top]
outer_loft_points = [outer_points_bottom, outer_points_top]

# Create inner wall surface
inner_wire_bottom = cq.Workplane("XY").polyline(wall_points_bottom).close().val()
inner_wire_top = cq.Workplane("XY").polyline(wall_points_top).close().val()

# Create outer wall surface
outer_wire_bottom = cq.Workplane("XY").polyline(outer_points_bottom).close().val()
outer_wire_top = cq.Workplane("XY").polyline(outer_points_top).close().val()

# Build scroll wall as extruded profile between inner and outer curves
# Create a profile that will be swept
profile_points = [
    (inner_edge_points[0][0], inner_edge_points[0][1], 0),
    (outer_edge_points[0][0], outer_edge_points[0][1], 0),
    (outer_edge_points[0][0], outer_edge_points[0][1], wall_height),
    (inner_edge_points[0][0], inner_edge_points[0][1], wall_height),
]

# Create the scroll wall by sweeping a rectangular profile along the centerline
sweep_path_points = []
for i in range(len(involute_points_2d)):
    x, y = involute_points_2d[i]
    sweep_path_points.append((x, y, plate_thickness))

# Create path as 3D wire
sweep_path = cq.Workplane("XY").polyline(sweep_path_points).val()

# Build wall by sweeping rectangular cross-section along path
profile_rect = (
    cq.Workplane("XY")
    .moveTo(-wall_thickness / 2, 0)
    .lineTo(wall_thickness / 2, 0)
    .lineTo(wall_thickness / 2, wall_height)
    .lineTo(-wall_thickness / 2, wall_height)
    .close()
)

# Use a simpler approach: create solid by layering
scroll_wall = cq.Workplane("XY")
for i in range(len(involute_points_2d) - 1):
    x1, y1 = involute_points_2d[i]
    x2, y2 = involute_points_2d[i + 1]
    
    angle_rad = math.radians((i / num_points) * involute_angle_max)
    tangent_x = -base_circle_radius * math.sin(angle_rad) + base_circle_radius * angle_rad * math.cos(angle_rad)
    tangent_y = base_circle_radius * math.cos(angle_rad) + base_circle_radius * angle_rad * math.sin(angle_rad)
    tangent_length = math.sqrt(tangent_x**2 + tangent_y**2)
    if tangent_length > 0.001:
        tangent_x /= tangent_length
        tangent_y /= tangent_length
    
    normal_x = -tangent_y
    normal_y = tangent_x
    
    i1_x = x1 - (wall_thickness / 2) * normal_x
    i1_y = y1 - (wall_thickness / 2) * normal_y
    o1_x = x1 + (wall_thickness / 2) * normal_x
    o1_y = y1 + (wall_thickness / 2) * normal_y
    
    angle_rad2 = math.radians(((i + 1) / num_points) * involute_angle_max)
    tangent_x2 = -base_circle_radius * math.sin(angle_rad2) + base_circle_radius * angle_rad2 * math.cos(angle_rad2)
    tangent_y2 = base_circle_radius * math.cos(angle_rad2) + base_circle_radius * angle_rad2 * math.sin(angle_rad2)
    tangent_length2 = math.sqrt(tangent_x2**2 + tangent_y2**2)
    if tangent_length2 > 0.001:
        tangent_x2 /= tangent_length2
        tangent_y2 /= tangent_length2
    
    normal_x2 = -tangent_y2
    normal_y2 = tangent_x2
    
    i2_x = x2 - (wall_thickness / 2) * normal_x2
    i2_y = y2 - (wall_thickness / 2) * normal_y2
    o2_x = x2 + (wall_thickness / 2) * normal_x2
    o2_y = y2 + (wall_thickness / 2) * normal_y2
    
    pts = [
        (i1_x, i1_y, plate_thickness),
        (o1_x, o1_y, plate_thickness),
        (o2_x, o2_y, plate_thickness),
        (i2_x, i2_y, plate_thickness),
        (i1_x, i1_y, plate_thickness + wall_height),
        (o1_x, o1_y, plate_thickness + wall_height),
        (o2_x, o2_y, plate_thickness + wall_height),
        (i2_x, i2_y, plate_thickness + wall_height),
    ]
    
    if i == 0:
        seg = cq.Workplane("XY").polyline(pts[:4]).close().extrude(wall_height)
        scroll_wall = seg
    else:
        seg = cq.Workplane("XY").polyline(pts[:4]).close().extrude(wall_height)
        scroll_wall = scroll_wall.union(seg)

# Combine plate and wall
result = plate.union(scroll_wall)
