import cadquery as cq
import math

# Create the base cylinder
base_cylinder = cq.Workplane("XY").cylinder(height=80, radius=15, centered=True)

# Create the helical groove
# Parameters
cylinder_radius = 15
groove_radius = 2  # semicircular cross-section radius
pitch = 20  # mm per turn
num_turns = 4
total_height = 80
length_per_turn = pitch

# Create points along the helix
helix_points = []
num_points_per_turn = 100
total_points = num_points_per_turn * num_turns

for i in range(total_points + 1):
    t = i / num_points_per_turn  # parameter from 0 to num_turns
    z = -total_height/2 + (t / num_turns) * total_height
    angle = t * 2 * math.pi
    
    # Center of the groove path on the cylinder surface
    x = cylinder_radius * math.cos(angle)
    y = cylinder_radius * math.sin(angle)
    
    helix_points.append((x, y, z))

# Create a sweep profile (semicircle for the groove cross-section)
profile = cq.Workplane("XY").circle(groove_radius)

# Create the groove by sweeping a circle along the helix path
groove_solid = None
for i in range(len(helix_points) - 1):
    p1 = helix_points[i]
    p2 = helix_points[i + 1]
    
    # Create a small cylinder segment along the helix
    length = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
    
    if groove_solid is None:
        groove_solid = cq.Workplane("XY").sphere(groove_radius).translate(p1)
    else:
        groove_solid = groove_solid.union(cq.Workplane("XY").sphere(groove_radius).translate(p1))

# Create a proper swept groove using multiple small spheres along the helix
groove_to_cut = None
for i in range(0, len(helix_points), 2):
    p = helix_points[i]
    sphere = cq.Workplane("XY").sphere(groove_radius).translate(p)
    if groove_to_cut is None:
        groove_to_cut = sphere
    else:
        groove_to_cut = groove_to_cut.union(sphere)

# Perform the cutting operation
result = base_cylinder.cut(groove_to_cut)
