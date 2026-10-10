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

# Create V-shaped groove profile (a simple triangle in cross-section)
groove_depth = 2
groove_width = 3

# Create first helical groove set
# We'll create multiple grooves by circular array

def create_helical_groove_edge(radius, pitch, turns, num_points=200):
    """Create a helical edge for sweeping"""
    points = []
    for i in range(num_points):
        t = i / num_points * turns * 2 * math.pi
        z = (t / (2 * math.pi)) * pitch
        x = radius * math.cos(t)
        y = radius * math.sin(t)
        points.append((x, y, z - length/2))
    return points

# Create the V-groove profile
def create_v_groove_profile():
    """Create a V-shaped profile for the groove"""
    profile = (cq.Workplane("XY")
               .moveTo(0, 0)
               .lineTo(groove_width/2, -groove_depth)
               .lineTo(-groove_width/2, -groove_depth)
               .close())
    return profile

# Build the part with grooves using sweep
result = cylinder

# Create first helical groove pattern (right-handed helix)
helix_points_1 = create_helical_groove_edge(helix_radius, pitch, num_turns)

# Create a wire from helix points
helix_wire_1 = cq.Wire.makePolyCurve(
    [cq.Vector(*pt) for pt in helix_points_1]
)

# Create profile for sweep
profile = cq.Workplane("XY").moveTo(0, 0).polygon(3, groove_width/math.sqrt(3)).val()

# Create sweep for first helical groove
try:
    sweep_1 = result.sweep(profile, helix_wire_1, isFrenet=True)
    result = result.cut(sweep_1)
except:
    pass

# Create second helical groove pattern (left-handed helix - reverse direction)
# Reverse the helix direction
helix_points_2 = []
for i in range(len(helix_points_1)):
    x, y, z = helix_points_1[i]
    # Mirror in XY and reverse the helical direction
    t = i / (len(helix_points_1)-1) * num_turns * 2 * math.pi
    z_new = (t / (2 * math.pi)) * pitch
    x_new = helix_radius * math.cos(-t)  # Reverse direction
    y_new = helix_radius * math.sin(-t)
    helix_points_2.append((x_new, y_new, z_new - length/2))

helix_wire_2 = cq.Wire.makePolyCurve(
    [cq.Vector(*pt) for pt in helix_points_2]
)

try:
    sweep_2 = result.sweep(profile, helix_wire_2, isFrenet=True)
    result = result.cut(sweep_2)
except:
    pass

# Create circular arrays of the grooves by rotating around the cylinder axis
num_arrays = 4
angle_step = 360 / num_arrays

result_with_arrays = result
for i in range(1, num_arrays):
    rotation_angle = i * angle_step
    rotated = result.rotate((0, 0, 0), (0, 0, 1), rotation_angle)
    try:
        result_with_arrays = result_with_arrays.union(rotated)
    except:
        pass

result = result_with_arrays
