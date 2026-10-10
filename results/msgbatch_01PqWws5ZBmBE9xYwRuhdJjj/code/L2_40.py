import cadquery as cq
import math

# Create the base cylinder
result = cq.Workplane("XY").cylinder(height=60, radius=15, centered=True)

# Parameters
radius = 15
height = 60
num_grooves = 8
pitch = 15  # helix pitch
turns = height / pitch

# Create V-shaped notch profile (2D cross-section)
notch_profile = (
    cq.Workplane("XY")
    .polyline([(0, 0), (1, -1.5), (2, 0)])
    .close()
)

# Create a helical sweep path for the first set of grooves
# We'll use approximation with a 3D wire
def create_helix(radius, height, turns, direction=1):
    """Create a helix path as a list of points"""
    points = []
    num_points = int(turns * 100)
    for i in range(num_points):
        t = i / num_points
        angle = t * turns * 2 * math.pi * direction
        z = (t - 0.5) * height
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y, z))
    return points

# Create first set of helical grooves (clockwise)
helix_points_cw = create_helix(radius - 2, height, turns, direction=1)

# Create the sweep path for the first helix
sweep_path_cw = cq.Workplane("XY").polyline(helix_points_cw)

# Create grooves using a circular array with helical pattern
# We'll use a different approach: create V-groove at different angles
base = result

# Create V-shaped groove profile in YZ plane at origin
groove_profile = cq.Workplane("YZ").polyline([
    (-1.5, -8),
    (0, -10),
    (1.5, -8)
]).close()

# Create first set of grooves using circular array
for i in range(num_grooves):
    angle = (360 / num_grooves) * i
    
    # Create a groove by sweeping V-profile along helix
    groove_points = create_helix(radius - 1.5, height, turns, direction=1)
    
    # Rotate groove points by the array angle
    rotated_points = []
    for (x, y, z) in groove_points:
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        rotated_points.append((new_x, new_y, z))
    
    # Create sweep path
    sweep_path = cq.Workplane("XY").polyline(rotated_points)
    
    # Create a simple V-notch cutter
    notch = cq.Workplane("YZ").polyline([(-1.2, 0), (0, -2.5), (1.2, 0)]).close()
    
    try:
        # Sweep the notch along the helix path
        swept = notch.sweep(sweep_path, isFrenet=True)
        base = base.cut(swept)
    except:
        pass

# Create second set of grooves (counter-clockwise) 
for i in range(num_grooves):
    angle = (360 / num_grooves) * i + (180 / num_grooves)
    
    # Create a groove with reverse helix
    groove_points = create_helix(radius - 1.5, height, turns, direction=-1)
    
    # Rotate groove points by the array angle
    rotated_points = []
    for (x, y, z) in groove_points:
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        rotated_points.append((new_x, new_y, z))
    
    # Create sweep path
    sweep_path = cq.Workplane("XY").polyline(rotated_points)
    
    # Create a simple V-notch cutter
    notch = cq.Workplane("YZ").polyline([(1.2, 0), (0, -2.5), (-1.2, 0)]).close()
    
    try:
        # Sweep the notch along the reverse helix path
        swept = notch.sweep(sweep_path, isFrenet=True)
        base = base.cut(swept)
    except:
        pass

result = base
