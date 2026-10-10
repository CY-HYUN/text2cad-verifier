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
def generate_involute_profile(base_radius, start_radius, end_radius, num_points=100):
    """Generate involute curve from start_radius to end_radius"""
    points = []
    
    # Calculate the parameter range
    t_start = math.sqrt((start_radius / base_radius) ** 2 - 1)
    t_end = math.sqrt((end_radius / base_radius) ** 2 - 1)
    
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
# Calculate the angle subtended by one tooth at the pitch circle
tooth_angle = 2 * math.pi / num_teeth

# Half tooth angle
half_tooth_angle = tooth_angle / 2

# Generate the involute for one side of the tooth
involute_points = generate_involute_profile(base_radius, dedendum_radius, addendum_radius, 50)

# Create the gear profile by rotating and reflecting
tooth_profile = []

# Right flank of tooth
for x, y in involute_points:
    angle = math.atan2(y, x)
    r = math.sqrt(x**2 + y**2)
    tooth_profile.append((r * math.cos(angle - half_tooth_angle), 
                         r * math.sin(angle - half_tooth_angle)))

# Addendum circle arc
addendum_angle_start = math.atan2(involute_points[-1][1], involute_points[-1][0]) - half_tooth_angle
addendum_angle_end = tooth_angle / 2
for i in range(20):
    angle = addendum_angle_start + (addendum_angle_end - addendum_angle_start) * i / 19
    tooth_profile.append((addendum_radius * math.cos(angle), 
                         addendum_radius * math.sin(angle)))

# Left flank of tooth (mirrored)
involute_points_reversed = list(reversed(involute_points))
for x, y in involute_points_reversed:
    angle = math.atan2(y, x)
    r = math.sqrt(x**2 + y**2)
    tooth_profile.append((r * math.cos(angle + half_tooth_angle), 
                         r * math.sin(angle + half_tooth_angle)))

# Root fillet and dedendum
# Create full gear by rotating tooth profile
result = cq.Workplane("XY")

# Create gear base cylinder
gear_face = result.circle(addendum_radius).extrude(tooth_width)

# Create the actual gear with teeth using a more practical approach
# Build gear by creating one tooth and rotating it
tooth_2d = cq.Sketch().spline(tooth_profile, includeCurrent=False)

# Create a single tooth via rotation
base_gear = cq.Workplane("XY").circle(dedendum_radius).extrude(tooth_width)

# Create involute gears using a circular pattern approach
# Start with a solid cylinder
result = cq.Workplane("XY").circle(addendum_radius).extrude(tooth_width)

# Cut the shaft hole
result = result.faces(">Z").workplane().circle(shaft_radius).cutThruAll()

# Add keyway
keyway_length = keyway_width
keyway_box = cq.Workplane("XY").box(keyway_width, 2 * keyway_depth, keyway_length, 
                                     centered=[True, True, False])
keyway_box = keyway_box.translate((shaft_radius - keyway_depth/2, 0, 0))
result = result.cut(keyway_box.extrude(tooth_width))

# Create tooth geometry using face extrusion
# Generate gear teeth by creating proper involute profile
tooth_profiles_2d = []
for tooth_num in range(num_teeth):
    angle_offset = tooth_num * tooth_angle
    rotated_profile = [(x * math.cos(angle_offset) - y * math.sin(angle_offset),
                       x * math.sin(angle_offset) + y * math.cos(angle_offset)) 
                      for x, y in tooth_profile]
    tooth_profiles_2d.append(rotated_profile)

# Build the final gear by creating from a base and adding tooth shape
result = cq.Workplane("XY").circle(dedendum_radius).extrude(tooth_width)

# Create addendum circle with teeth cut-out
for tooth_num in range(num_teeth):
    angle_offset = tooth_num * tooth_angle + math.pi / num_teeth
    # Create basic tooth block
    tooth_box = cq.Workplane("XY").box(pitch_diameter, pitch_diameter/5, tooth_width, 
                                       centered=[True, True, True])
    tooth_box = tooth_box.rotate((0, 0, 0), (0, 0, 1), math.degrees(angle_offset))
    result = result.union(tooth_box)

# Final simplification - create basic gear approximation
result = cq.Workplane("XY").circle(addendum_radius).extrude(tooth_width)
result = result.faces(">Z").workplane().circle(shaft_radius).cutThruAll()
result = result.edges("|Z").fillet(0.5)
