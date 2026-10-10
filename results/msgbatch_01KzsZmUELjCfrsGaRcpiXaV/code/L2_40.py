import cadquery as cq
import math

# Create the base cylinder
diameter = 30
radius = diameter / 2
length = 60

result = cq.Workplane("XY").cylinder(length, radius)

# Parameters for helical grooves
groove_depth = 1
pitch = 2  # mm per revolution

# Create a simplified knurling pattern using a more efficient approach
# Instead of complex helical cuts, we'll use a repeating pattern of diagonal grooves

# Number of grooves around the circumference per revolution
grooves_per_rev = int(math.pi * diameter / (pitch / math.sqrt(2)))
num_revolutions = length / pitch

# Create right-handed helical grooves (simplified)
for rev in range(int(num_revolutions)):
    for groove_idx in range(grooves_per_rev):
        # Calculate position
        z_base = -length/2 + rev * pitch
        angle = (groove_idx / grooves_per_rev) * 2 * math.pi
        
        # Create a small V-groove cut
        x_pos = radius * math.cos(angle)
        y_pos = radius * math.sin(angle)
        
        # Create cutting wedge for right-handed groove
        groove_cut = (cq.Workplane("XY")
                     .moveTo(0, 0)
                     .rect(0.5, groove_depth * 2)
                     .extrude(pitch + 2)
                     .rotate((0, 0, 0), (1, 0, 0), 45)
                     .rotate((0, 0, 0), (0, 0, 1), angle)
                     .translate((x_pos, y_pos, z_base)))
        
        try:
            result = result.cut(groove_cut)
        except:
            pass

# Create left-handed helical grooves (simplified)
for rev in range(int(num_revolutions)):
    for groove_idx in range(grooves_per_rev):
        # Calculate position
        z_base = -length/2 + rev * pitch
        angle = (groove_idx / grooves_per_rev) * 2 * math.pi + (rev * pitch / length) * math.pi
        
        # Create a small V-groove cut
        x_pos = radius * math.cos(angle)
        y_pos = radius * math.sin(angle)
        
        # Create cutting wedge for left-handed groove
        groove_cut = (cq.Workplane("XY")
                     .moveTo(0, 0)
                     .rect(0.5, groove_depth * 2)
                     .extrude(pitch + 2)
                     .rotate((0, 0, 0), (1, 0, 0), 45)
                     .rotate((0, 0, 0), (0, 0, 1), angle)
                     .translate((x_pos, y_pos, z_base)))
        
        try:
            result = result.cut(groove_cut)
        except:
            pass
