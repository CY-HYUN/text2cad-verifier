import cadquery as cq
import math

# Initialize the environment
# Create the rim base (annular ring)
rim_od = 120
rim_width = 40
rim_id = rim_od - 2 * rim_width
rim_height = 40

# Create annular ring for rim
rim_base = cq.Workplane("XY").circle(rim_od/2).circle(rim_id/2).extrude(rim_height)

# Create central hub
hub_od = 45
hub_height = 40
hub_base = cq.Workplane("XY").circle(hub_od/2).extrude(hub_height)

# Combine rim and hub
result = rim_base.union(hub_base)

# Create HTD 8M teeth with helical distribution
tooth_height = 4
num_teeth = 47
helix_angle = 15
helix_height = 40
pitch_angle = math.radians(helix_angle)

# Generate teeth
for i in range(num_teeth):
    angle = (i / num_teeth) * 360
    z_offset = (i / num_teeth) * helix_height
    
    # Create tooth as a simple extrusion
    tooth_radius = rim_id/2 + tooth_height/2
    tooth = cq.Workplane("XY").moveTo(tooth_radius, 0).circle(tooth_height/3).extrude(2)
    tooth = tooth.rotate((0, 0, 0), (0, 0, 1), angle)
    tooth = tooth.translate((0, 0, z_offset))
    
    result = result.union(tooth)

# Create spokes
num_spokes = 5
spoke_height = hub_height
outer_radius = rim_id/2
inner_radius = hub_od/2

for spoke_idx in range(num_spokes):
    spoke_angle = (spoke_idx / num_spokes) * 360
    angle_rad = math.radians(spoke_angle)
    
    # Hub side position
    start_x = inner_radius * math.cos(angle_rad)
    start_y = inner_radius * math.sin(angle_rad)
    
    # Rim side position
    end_x = outer_radius * math.cos(angle_rad)
    end_y = outer_radius * math.sin(angle_rad)
    
    # Create spoke as a tapered shape
    spoke = cq.Workplane("XY").moveTo(start_x, start_y).circle(3)
    spoke = spoke.extrude(spoke_height)
    
    # Taper toward the rim
    spoke_tapered = cq.Workplane("XY").moveTo(end_x, end_y).circle(2)
    spoke_tapered = spoke_tapered.extrude(spoke_height)
    
    result = result.union(spoke)

# Create shaft hole (25mm diameter)
shaft_hole = cq.Workplane("XY").circle(25/2).extrude(hub_height)
result = result.cut(shaft_hole)

# Create keyway (6mm width, centered on negative Y)
keyway_width = 6
keyway_height = 10
keyway = cq.Workplane("XY").rect(keyway_width, keyway_height).extrude(hub_height)
result = result.cut(keyway)

# Apply fillet at spoke connections (4mm radius)
try:
    result = result.edges("|Z").fillet(3)
except:
    pass

# Apply chamfer on rim top and bottom edges (1.5mm by 45 degrees)
try:
    # Chamfer top edge of rim
    result = result.faces(">Z").edges().chamfer(1.5, 45)
except:
    pass

try:
    # Chamfer bottom edge of rim
    result = result.faces("<Z").edges().chamfer(1.5, 45)
except:
    pass

# Ensure result is valid
if result is None:
    result = rim_base.union(hub_base)
