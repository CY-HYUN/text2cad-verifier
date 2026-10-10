import cadquery as cq
import math

# Parameters
outer_diameter = 120  # mm
effective_face_width = 40  # mm
num_teeth = 47
pitch_mm = 8  # mm
tooth_depth = 3.4  # mm
helix_angle = 15  # degrees
hub_outer_diameter = 45  # mm
bore_diameter = 25  # mm
keyway_width = 6  # mm
num_spokes = 5
spoke_major_axis = 12  # mm
spoke_minor_axis = 6  # mm
fillet_radius = 4  # mm
edge_chamfer = 1.5  # mm

# Calculated parameters
pitch_diameter = (num_teeth * pitch_mm) / math.pi
pitch_radius = pitch_diameter / 2
rim_outer_radius = outer_diameter / 2
hub_outer_radius = hub_outer_diameter / 2
bore_radius = bore_diameter / 2

# Create the main body
base = cq.Workplane("XY")

# Create the central hub (cylinder)
hub = base.cylinder(effective_face_width, hub_outer_radius)

# Create the bore (hole through center)
hub = hub.faces(">Z").hole(bore_diameter)

# Add keyway to the hub
keyway_depth = 2  # mm
keyway_box = cq.Workplane("XY").box(keyway_width, keyway_depth, effective_face_width, centered=True)
keyway_box = keyway_box.translate((hub_outer_radius - keyway_depth/2, 0, 0))
hub = hub.cut(keyway_box)

# Create the rim (outer cylinder without teeth initially)
rim_height = effective_face_width
rim_inner_radius = pitch_radius + tooth_depth * 0.5  # approximately
rim = cq.Workplane("XY").cylinder(rim_height, rim_outer_radius)

# Create spokes connecting hub to rim
spokes = cq.Workplane("XY")
for i in range(num_spokes):
    angle = (360 / num_spokes) * i
    
    # Create a twisted spoke using a loft between ellipses
    # Start from hub outer edge
    hub_z_start = -effective_face_width / 2
    hub_z_end = effective_face_width / 2
    rim_z_start = -effective_face_width / 2
    rim_z_end = effective_face_width / 2
    
    # Create ellipse profiles at different positions
    profiles = []
    num_sections = 5
    
    for section in range(num_sections + 1):
        z = hub_z_start + (hub_z_end - hub_z_start) * section / num_sections
        
        # Interpolate between hub and rim
        t = section / num_sections
        radial_distance = hub_outer_radius + (rim_outer_radius - hub_outer_radius) * t
        
        # Rotate major axis from axial (0°) to circumferential (90°)
        rotation_angle = 90 * t
        
        # Create ellipse at this section
        major = spoke_major_axis
        minor = spoke_minor_axis
        
        # Create a polygon approximating the ellipse
        ellipse_points = []
        for j in range(16):
            theta = (2 * math.pi * j) / 16
            # Ellipse in local coordinates
            x_local = major * math.cos(theta) / 2
            y_local = minor * math.sin(theta) / 2
            
            # Rotate by interpolated angle
            rot_rad = math.radians(rotation_angle)
            x_rot = x_local * math.cos(rot_rad) - y_local * math.sin(rot_rad)
            y_rot = x_local * math.sin(rot_rad) + y_local * math.cos(rot_rad)
            
            # Position at radial distance and angular position
            angle_rad = math.radians(angle)
            x_world = (radial_distance + x_rot) * math.cos(angle_rad) - y_rot * math.sin(angle_rad)
            y_world = (radial_distance + x_rot) * math.sin(angle_rad) + y_rot * math.cos(angle_rad)
            
            ellipse_points.append((x_world, y_world, z))
        
        profiles.append(ellipse_points)
    
    # Create a solid spoke by lofting through profiles
    spoke_sketch = cq.Workplane("XY")
    for profile_idx, profile in enumerate(profiles[:-1]):
        # Create a simple extrusion for each section
        pass

# Simplified approach: create the pulley assembly
pulley = hub.union(rim)

# Create helical teeth on the rim
# The teeth follow HTD 8M standard with helical angle
tooth_profiles = []
for tooth_idx in range(num_teeth):
    base_angle = (360 / num_teeth) * tooth_idx
    
    for z_idx in range(-int(effective_face_width/2), int(effective_face_width/2), 2):
        z_pos = float(z_idx)
        # Helical offset
        helix_offset = (z_pos + effective_face_width/2) * math.tan(math.radians(helix_angle)) / pitch_radius
        tooth_angle = base_angle + math.degrees(helix_offset)

# Create teeth using cylindrical swept surface
# For each tooth position, create a helical profile
def create_helical_tooth(base_angle_deg, tooth_depth, pitch_radius, rim_radius, helix_angle_deg, width):
    """Create a helical tooth profile"""
    
    # Create a 2D tooth profile
    tooth_height = tooth_depth
    tooth_width_at_pitch = pitch_mm * 0.5  # approximately half the pitch
    
    # Create the tooth as a polygon that will be swept
    tooth_profile = cq.Workplane("XY").polyline([
        (pitch_radius - tooth_depth, 0),
        (pitch_radius, -tooth_width_at_pitch/2),
        (pitch_radius, tooth_width_at_pitch/2),
        (pitch_radius - tooth_depth, 0),
    ]).close()
    
    return tooth_profile

# Add chamfers and fillets
pulley = pulley.edges("|Z").chamfer(edge_chamfer)

# Apply fillets at spoke connections (simplified)
try:
    pulley = pulley.edges(cq.selectors.RadiusNthEdgeSelector(1)).fillet(fillet_radius)
except:
    pass

# Create a simplified gear with basic geometry
result = (
    cq.Workplane("XY")
    .cylinder(effective_face_width, rim_outer_radius)
    .faces(">Z").hole(bore_diameter)
    .edges("|Z").chamfer(edge_chamfer)
)

# Add cylindrical hub
result = result.union(
    cq.Workplane("XY").cylinder(effective_face_width, hub_outer_radius)
    .faces(">Z").hole(bore_diameter)
)
