import cadquery as cq
import math

# Initialize the environment
# Create the rim base (annular ring)
rim_od = 120
rim_id = rim_od - 2 * 40  # width is 40mm, so inner diameter
rim_height = 40

# Create annular ring for rim
rim_base = cq.Workplane("XY").circle(rim_od/2).circle(rim_id/2).extrude(rim_height)

# Create central hub
hub_od = 45
hub_height = 40
hub_base = cq.Workplane("XY").circle(hub_od/2).extrude(hub_height)

# Combine rim and hub
result = rim_base.union(hub_base)

# Create HTD 8M tooth profile (approximate arc-based tooth)
# HTD 8M: 8mm pitch, standard tooth profile
tooth_height = 4
tooth_width = 3
num_teeth = 47

# Create a single tooth profile (arc approximation)
tooth_profile = cq.Workplane("XY").moveTo(rim_id/2 + tooth_height, 0)
tooth_profile = tooth_profile.radiusArc((rim_id/2 + tooth_height - tooth_width/2, 0), tooth_width/2)
tooth_profile = tooth_profile.lineTo(rim_id/2 + tooth_height, tooth_width/4)
tooth_profile = tooth_profile.close()

# Create helical sweep path
helix_angle = 15
helix_height = 40
pitch_angle = math.radians(helix_angle)

# Generate teeth with helical distribution
for i in range(num_teeth):
    angle = (i / num_teeth) * 360
    z_offset = (i / num_teeth) * helix_height
    
    # Create tooth at angular position with helical offset
    tooth = cq.Workplane("XY").moveTo(rim_id/2, 0).radiusArc(
        (rim_id/2 + tooth_height * math.cos(pitch_angle), tooth_height * math.sin(pitch_angle)), 
        tooth_height
    )
    tooth_3d = tooth.extrude(2)
    
    # Rotate and position tooth
    tooth_3d = tooth_3d.rotate((0, 0, 0), (0, 0, 1), angle)
    tooth_3d = tooth_3d.translate((0, 0, z_offset))
    
    result = result.union(tooth_3d)

# Create spokes
num_spokes = 5
spoke_height = hub_height

# Outer reference plane on rim inner edge
outer_radius = rim_id/2
inner_radius = hub_od/2

for spoke_idx in range(num_spokes):
    spoke_angle = (spoke_idx / num_spokes) * 360
    
    # Create elliptical sections
    # Start section (major axis axial, minor axis circumferential)
    start_x = inner_radius * math.cos(math.radians(spoke_angle))
    start_y = inner_radius * math.sin(math.radians(spoke_angle))
    
    end_x = outer_radius * math.cos(math.radians(spoke_angle))
    end_y = outer_radius * math.sin(math.radians(spoke_angle))
    
    # Create start ellipse at hub
    start_ellipse = cq.Workplane("XY").moveTo(start_x, start_y)
    start_ellipse = start_ellipse.ellipse(12, 6)  # major=12, minor=6
    start_ellipse = start_ellipse.extrude(0.1)
    
    # Create end ellipse at rim (rotated 90 degrees)
    end_ellipse = cq.Workplane("XY").moveTo(end_x, end_y)
    end_ellipse = end_ellipse.ellipse(6, 12)  # rotated: major=6 (circumferential), minor=12 (axial)
    end_ellipse = end_ellipse.extrude(0.1)
    
    # Create lofted spoke connecting the two sections
    spoke = cq.Workplane("XY").polyline(
        [(start_x, start_y, 0), (end_x, end_y, spoke_height)]
    ).sweep(cq.Workplane("XY").circle(3))
    
    result = result.union(spoke)

# Create shaft hole (25mm diameter)
shaft_hole = cq.Workplane("XY").circle(25/2).extrude(hub_height)
result = result.cut(shaft_hole)

# Create keyway (6mm width)
keyway = cq.Workplane("XY").rect(6, 10).extrude(hub_height)
keyway = keyway.translate((25/2 - 3, 0, 0))
result = result.cut(keyway)

# Apply fillets at spoke roots
result = result.edges("|Z").fillet(4)

# Apply chamfer on rim edges
result = result.edges(">>Z").chamfer(1.5, 45)

# Final result
result = result
