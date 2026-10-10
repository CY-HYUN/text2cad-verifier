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

# Create the main rim (outer cylinder)
rim = cq.Workplane("XY").cylinder(effective_face_width, rim_outer_radius)

# Create the hub (inner cylinder)
hub = cq.Workplane("XY").cylinder(effective_face_width, hub_outer_radius)

# Combine rim and hub
pulley = rim.union(hub)

# Cut the central bore
pulley = pulley.faces(">Z").hole(bore_diameter)

# Add keyway to the hub
keyway_depth = 2  # mm
keyway = (
    cq.Workplane("XY")
    .box(keyway_width, keyway_depth, effective_face_width, centered=True)
    .translate((hub_outer_radius - keyway_depth / 2, 0, 0))
)
pulley = pulley.cut(keyway)

# Create spokes connecting hub to rim
spoke_angles = [360 / num_spokes * i for i in range(num_spokes)]

for spoke_angle_deg in spoke_angles:
    spoke_angle_rad = math.radians(spoke_angle_deg)
    
    # Create spoke geometry using multiple sections
    num_sections = 6
    
    # Build spoke by creating and unioning multiple rectangular boxes with rotation
    for section_idx in range(num_sections - 1):
        t = section_idx / (num_sections - 1)
        next_t = (section_idx + 1) / (num_sections - 1)
        
        # Position along radial direction
        z_center = -effective_face_width / 2 + effective_face_width / 2
        
        # Interpolate radius from hub to rim
        current_radius = hub_outer_radius + (rim_outer_radius - hub_outer_radius) * t
        next_radius = hub_outer_radius + (rim_outer_radius - hub_outer_radius) * next_t
        
        # Create a tapered section
        section_length = (next_radius - current_radius) * 1.1
        section_center_radius = (current_radius + next_radius) / 2
        
        # Rotation angle for twist (major axis rotates 90 degrees from hub to rim)
        twist_angle = 90 * t
        
        # Create spoke section as a rotated box
        spoke_section = (
            cq.Workplane("XY")
            .box(spoke_major_axis, spoke_minor_axis, effective_face_width, centered=True)
            .rotate((0, 0, 1), (0, 0, 0), twist_angle)
            .translate((section_center_radius, 0, 0))
            .rotate((0, 0, 1), (0, 0, 0), spoke_angle_deg)
        )
        
        pulley = pulley.union(spoke_section)

# Add teeth to the rim surface
# Create a simplified tooth pattern using Boolean operations
for tooth_idx in range(num_teeth):
    tooth_angle_deg = 360 / num_teeth * tooth_idx
    tooth_angle_rad = math.radians(tooth_angle_deg)
    
    # Helical offset varies with Z position
    for z_offset in range(-int(effective_face_width / 2) + 1, int(effective_face_width / 2), 4):
        z_norm = (z_offset + effective_face_width / 2) / effective_face_width
        helix_offset_rad = z_norm * math.tan(math.radians(helix_angle)) * (pitch_mm / pitch_radius)
        
        tooth_angle_with_helix = tooth_angle_rad + helix_offset_rad
        
        # Create tooth as a small tapered cylinder
        tooth_x = (rim_outer_radius - tooth_depth / 2) * math.cos(tooth_angle_with_helix)
        tooth_y = (rim_outer_radius - tooth_depth / 2) * math.sin(tooth_angle_with_helix)
        
        tooth = (
            cq.Workplane("XY")
            .cylinder(2, tooth_depth / 2)
            .translate((tooth_x, tooth_y, z_offset))
        )
        
        pulley = pulley.cut(tooth)

# Chamfer the top and bottom edges of the rim
try:
    pulley = pulley.faces(">Z").chamfer(edge_chamfer)
except:
    pass

try:
    pulley = pulley.faces("<Z").chamfer(edge_chamfer)
except:
    pass

# Apply fillets to internal edges where possible
try:
    pulley = pulley.edges(cq.selectors.RadiusNthEdgeSelector(0)).fillet(fillet_radius)
except:
    pass

result = pulley
