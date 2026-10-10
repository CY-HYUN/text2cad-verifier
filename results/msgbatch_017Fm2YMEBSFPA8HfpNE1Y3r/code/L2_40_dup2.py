import cadquery as cq
import math

# Create the base cylinder
diameter = 30
radius = diameter / 2
length = 60

cylinder = cq.Workplane("XY").cylinder(height=length, radius=radius)

# Define helical path parameters
helix_radius = radius - 2  # Slightly inset from the cylinder surface
pitch = 10  # mm per revolution
num_turns = length / pitch

# Create V-shaped groove profile parameters
groove_depth = 2
groove_width = 3

def create_helical_groove_edge(radius, pitch, turns, num_points=200):
    """Create a helical edge for sweeping"""
    points = []
    for i in range(num_points):
        t = i / num_points * turns * 2 * math.pi
        z = (t / (2 * math.pi)) * pitch
        x = radius * math.cos(t)
        y = radius * math.sin(t)
        points.append(cq.Vector(x, y, z - length/2))
    return points

# Create first helical groove pattern (right-handed helix)
helix_points_1 = create_helical_groove_edge(helix_radius, pitch, num_turns)

# Create a wire from helix points
try:
    helix_wire_1 = cq.Wire.assembleEdges(
        [cq.Edge.makeLine(helix_points_1[i], helix_points_1[i+1]) 
         for i in range(len(helix_points_1)-1)]
    )
except:
    # Fallback: create edge points differently
    helix_wire_1 = cq.Workplane().polyline(helix_points_1).val()

# Create V-shaped profile for sweep
profile_2d = (cq.Workplane("XY")
              .moveTo(0, 0)
              .lineTo(groove_width/2, -groove_depth)
              .lineTo(-groove_width/2, -groove_depth)
              .close()
              .val())

# Start with the base cylinder
result = cylinder

# Try to create sweep for first helical groove
try:
    sweep_1 = result.sweep(profile_2d, helix_wire_1, isFrenet=True)
    result = result.cut(sweep_1)
except:
    pass

# Create second helical groove pattern (left-handed helix - reverse direction)
helix_points_2 = []
num_pts = len(helix_points_1)
for i in range(num_pts):
    progress = i / (num_pts - 1) if num_pts > 1 else 0
    t = progress * num_turns * 2 * math.pi
    z_new = (t / (2 * math.pi)) * pitch
    x_new = helix_radius * math.cos(-t)  # Reverse direction
    y_new = helix_radius * math.sin(-t)
    helix_points_2.append(cq.Vector(x_new, y_new, z_new - length/2))

# Create wire for second helix
try:
    helix_wire_2 = cq.Wire.assembleEdges(
        [cq.Edge.makeLine(helix_points_2[i], helix_points_2[i+1]) 
         for i in range(len(helix_points_2)-1)]
    )
except:
    helix_wire_2 = cq.Workplane().polyline(helix_points_2).val()

# Create sweep for second helical groove
try:
    sweep_2 = result.sweep(profile_2d, helix_wire_2, isFrenet=True)
    result = result.cut(sweep_2)
except:
    pass

# Create circular arrays of the grooves by rotating around the cylinder axis
num_arrays = 4
angle_step = 360 / num_arrays

result_final = result
for i in range(1, num_arrays):
    rotation_angle = i * angle_step
    rotated = result.rotate((0, 0, 0), (0, 0, 1), rotation_angle)
    try:
        result_final = result_final.union(rotated)
    except:
        pass

result = result_final
