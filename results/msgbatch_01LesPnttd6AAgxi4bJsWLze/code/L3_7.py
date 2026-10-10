import cadquery as cq
import math

# Parameters
base_circle_radius = 3  # mm
involute_angle_max = 1080  # degrees (3 turns)
wall_thickness = 4  # mm
wall_height = 25  # mm
plate_diameter = 80  # mm
plate_thickness = 5  # mm
closing_radius = 2  # mm for semicircle closure

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
num_points = 360
involute_points = []
for i in range(num_points + 1):
    angle = (i / num_points) * involute_angle_max
    x, y = involute_point(angle, base_circle_radius)
    involute_points.append((x, y, 0))

# Create the centerline as a 3D spline
centerline = cq.Workplane("XY").spline(involute_points)

# For the scroll wall, we need to create an offset profile and sweep it
# Create a 2D profile (the wall cross-section) at the starting point
start_x, start_y = involute_point(0, base_circle_radius)
start_angle = math.atan2(base_circle_radius, 0)  # tangent angle at start

# Create wall profile perpendicular to the involute at each point
# The wall has thickness 'wall_thickness' on each side of the centerline

def create_wall_profile_at_point(angle_deg, base_radius, thickness, height):
    """Create a rectangular profile perpendicular to involute at given angle"""
    angle_rad = math.radians(angle_deg)
    
    # Tangent direction of involute
    tangent_x = -base_radius * math.sin(angle_rad) + base_radius * angle_rad * math.cos(angle_rad)
    tangent_y = base_radius * math.cos(angle_rad) + base_radius * angle_rad * math.sin(angle_rad)
    
    # Normalize tangent
    tangent_length = math.sqrt(tangent_x**2 + tangent_y**2)
    tangent_x /= tangent_length
    tangent_y /= tangent_length
    
    # Normal direction (perpendicular to tangent)
    normal_x = -tangent_y
    normal_y = tangent_x
    
    return (normal_x, normal_y, tangent_x, tangent_y)

# Build the scroll wall using a swept surface approach
# Create a polyline for the inner edge and outer edge of the wall

inner_edge = []
outer_edge = []

for i in range(num_points + 1):
    angle = (i / num_points) * involute_angle_max
    x, y = involute_point(angle, base_circle_radius)
    
    normal_x, normal_y, _, _ = create_wall_profile_at_point(angle, base_circle_radius, wall_thickness, wall_height)
    
    # Inner and outer edges of the wall
    inner_x = x - (wall_thickness / 2) * normal_x
    inner_y = y - (wall_thickness / 2) * normal_y
    outer_x = x + (wall_thickness / 2) * normal_x
    outer_y = y + (wall_thickness / 2) * normal_y
    
    inner_edge.append((inner_x, inner_y, plate_thickness))
    outer_edge.append((outer_x, outer_y, plate_thickness))

# Create a wire for inner and outer edges
inner_wire = cq.Workplane("XY").polyline(inner_edge).val()
outer_wire = cq.Workplane("XY").polyline(outer_edge).val()

# Extrude the wall profile
wall_profile = cq.Workplane("XY").polyline(inner_edge + list(reversed(outer_edge)) + [inner_edge[0]]).close().extrude(wall_height)

# Create the scroll using a different approach: loft between inner and outer edges at different heights
wall = cq.Workplane("XY")

# Build scroll wall as a series of lofted surfaces
for i in range(num_points):
    angle1 = (i / num_points) * involute_angle_max
    angle2 = ((i + 1) / num_points) * involute_angle_max
    
    x1, y1 = involute_point(angle1, base_circle_radius)
    x2, y2 = involute_point(angle2, base_circle_radius)
    
    # Create rectangular segments
    n1x, n1y, _, _ = create_wall_profile_at_point(angle1, base_circle_radius, wall_thickness, wall_height)
    n2x, n2y, _, _ = create_wall_profile_at_point(angle2, base_circle_radius, wall_thickness, wall_height)
    
    i1_x = x1 - (wall_thickness / 2) * n1x
    i1_y = y1 - (wall_thickness / 2) * n1y
    o1_x = x1 + (wall_thickness / 2) * n1x
    o1_y = y1 + (wall_thickness / 2) * n1y
    
    i2_x = x2 - (wall_thickness / 2) * n2x
    i2_y = y2 - (wall_thickness / 2) * n2y
    o2_x = x2 + (wall_thickness / 2) * n2x
    o2_y = y2 + (wall_thickness / 2) * n2y
    
    # Create a box for this segment
    pts = [
        (i1_x, i1_y, plate_thickness),
        (o1_x, o1_y, plate_thickness),
        (o2_x, o2_y, plate_thickness),
        (i2_x, i2_y, plate_thickness),
    ]

# Simplified approach: create wall as an extruded offset surface
scroll_wall = cq.Workplane("XY").polyline(
    [(x, y, 0) for x, y in involute_points] if involute_points else [(0, 0, 0)]
).extrude(wall_height)

# Combine plate and wall
result = plate.union(scroll_wall)
