import cadquery as cq
import math

# Gear parameters
module = 3
num_teeth = 20
pressure_angle = 20  # degrees
tooth_width = 15  # mm
pitch_diameter = 60  # mm
addendum_diameter = 66  # mm
dedendum_diameter = 52.5  # mm
shaft_hole_diameter = 20  # mm
keyway_width = 6  # mm
keyway_depth = 3  # mm
root_fillet_radius = 0.9  # mm

# Convert pressure angle to radians
pressure_angle_rad = math.radians(pressure_angle)

# Calculate radii
pitch_radius = pitch_diameter / 2
addendum_radius = addendum_diameter / 2
dedendum_radius = dedendum_diameter / 2
shaft_radius = shaft_hole_diameter / 2

# Base circle radius for involute
base_radius = pitch_radius * math.cos(pressure_angle_rad)

# Generate involute tooth profile
def generate_involute_profile(base_radius, start_radius, end_radius, num_points=50):
    """Generate involute curve from start_radius to end_radius"""
    points = []
    
    # Ensure start_radius >= base_radius to avoid domain error
    start_radius = max(start_radius, base_radius + 0.1)
    end_radius = max(end_radius, base_radius + 0.1)
    
    # Calculate the parameter range
    t_start = math.sqrt(max(0, (start_radius / base_radius) ** 2 - 1))
    t_end = math.sqrt(max(0, (end_radius / base_radius) ** 2 - 1))
    
    for i in range(num_points):
        t = t_start + (t_end - t_start) * i / (num_points - 1)
        
        # Involute parametric equations
        r = base_radius * math.sqrt(1 + t**2)
        theta = math.atan(t) - t
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))
    
    return points

# Generate one tooth profile
tooth_angle = 2 * math.pi / num_teeth
half_tooth_angle = tooth_angle / 2

# Generate the involute for one side of the tooth
involute_points = generate_involute_profile(base_radius, dedendum_radius, addendum_radius, 40)

# Create tooth profile
tooth_profile = []

# Right flank of tooth
for x, y in involute_points:
    angle = math.atan2(y, x)
    r = math.sqrt(x**2 + y**2)
    tooth_profile.append((r * math.cos(angle - half_tooth_angle), 
                         r * math.sin(angle - half_tooth_angle)))

# Addendum circle arc
num_arc_points = 15
addendum_angle_start = math.atan2(involute_points[-1][1], involute_points[-1][0]) - half_tooth_angle
addendum_angle_end = half_tooth_angle

for i in range(num_arc_points):
    angle = addendum_angle_start + (addendum_angle_end - addendum_angle_start) * i / (num_arc_points - 1)
    tooth_profile.append((addendum_radius * math.cos(angle), 
                         addendum_radius * math.sin(angle)))

# Left flank of tooth (mirrored)
involute_points_reversed = list(reversed(involute_points))
for x, y in involute_points_reversed:
    angle = math.atan2(y, x)
    r = math.sqrt(x**2 + y**2)
    tooth_profile.append((r * math.cos(angle + half_tooth_angle), 
                         r * math.sin(angle + half_tooth_angle)))

# Start with base cylinder at dedendum radius
result = cq.Workplane("XY").circle(dedendum_radius).extrude(tooth_width)

# Add each tooth
for tooth_num in range(num_teeth):
    angle_offset = tooth_num * tooth_angle
    
    # Rotate tooth profile
    rotated_profile = []
    for x, y in tooth_profile:
        x_rot = x * math.cos(angle_offset) - y * math.sin(angle_offset)
        y_rot = x * math.sin(angle_offset) + y * math.cos(angle_offset)
        rotated_profile.append((x_rot, y_rot))
    
    # Close the profile by connecting back to dedendum
    rotated_profile.append((dedendum_radius * math.cos(angle_offset + half_tooth_angle),
                           dedendum_radius * math.sin(angle_offset + half_tooth_angle)))
    rotated_profile.append((dedendum_radius * math.cos(angle_offset - half_tooth_angle),
                           dedendum_radius * math.sin(angle_offset - half_tooth_angle)))
    
    # Create tooth face and extrude
    tooth_face = cq.Workplane("XY").spline(rotated_profile, includeCurrent=False).close()
    tooth_solid = tooth_face.extrude(tooth_width)
    result = result.union(tooth_solid)

# Cut the shaft hole
result = result.faces(">Z").workplane().circle(shaft_radius).cutThruAll()

# Add keyway at one tooth space
keyway_y_offset = shaft_radius
keyway_box = cq.Workplane("XY").box(keyway_width, keyway_depth, tooth_width, 
                                     centered=[True, True, True])
keyway_box = keyway_box.translate((shaft_radius - keyway_depth/2, 0, 0))
result = result.cut(keyway_box)

# Add root fillets
result = result.edges("|Z").fillet(root_fillet_radius)

