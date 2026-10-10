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
num_revolutions = length / pitch
groove_angle = 45  # degrees

# Create a function to generate helical groove cutting patterns
def create_helical_grooves(workplane, radius, length, pitch, groove_depth, handedness):
    """
    handedness: 1 for right-handed, -1 for left-handed
    """
    # We'll create the grooves by making a series of diagonal cuts
    # that follow a helical pattern on the cylinder surface
    
    # Convert cylinder to a shape we can work with
    shape = workplane
    
    # Number of helical turns
    num_turns = length / pitch
    
    # Create cutting geometry - helical V-grooves
    # We'll approximate this with multiple angled cuts
    steps = int(num_turns * 12)  # 12 steps per revolution for smoothness
    
    for i in range(steps):
        # Position along the length
        z_pos = (i / steps) * length - length/2
        
        # Angle around the cylinder (in radians)
        angle_around = (i / steps) * num_turns * 2 * math.pi
        
        # Create a plane that cuts at 45 degrees along the helix
        # This plane will be rotated around the Z axis and tilted
        rotation_angle = handedness * angle_around * 180 / math.pi
        
        # For right-handed: groove goes from lower-left to upper-right when looking along axis
        # For left-handed: groove goes from lower-right to upper-left
        
        # Create a cutting box at this position
        if i % 6 == 0:  # Reduce number of cuts for performance
            # Create a diagonal cutting plane
            cutting_plane = (cq.Workplane("XY")
                           .moveTo(0, 0)
                           .rect(diameter + 2, groove_depth * 2)
                           .extrude(length + 2)
                           .rotate((0, 0, 0), (0, 0, 1), rotation_angle)
                           .translate((0, 0, z_pos)))
            
            try:
                shape = shape.cut(cutting_plane)
            except:
                pass  # Skip if cut fails
    
    return shape

# Apply right-handed helical grooves
result = create_helical_grooves(result, radius, length, pitch, groove_depth, 1)

# Apply left-handed helical grooves
result = create_helical_grooves(result, radius, length, pitch, groove_depth, -1)

# Alternative simpler approach: use spiral pattern with cutting
# Create the base cylinder
result = cq.Workplane("XY").cylinder(length, radius)

# Approximate the knurling pattern with a series of V-groove cuts
# Create helical cutting edges
num_helices_per_direction = int(length / pitch * 2)  # Multiple helices covering the length

# For each direction of helices
for direction in [1, -1]:  # right-handed and left-handed
    for helix_num in range(num_helices_per_direction):
        # Create a thin cutting shape that spirals around the cylinder
        points = []
        steps_per_helix = 36  # Points along one helix
        
        for step in range(steps_per_helix * int(length / pitch)):
            # Parameter along the helix
            t = step / steps_per_helix
            
            # Z position (along cylinder axis)
            z = (t * length / (length / pitch)) - length/2
            
            # Angle around cylinder
            theta = direction * t * 2 * math.pi
            
            # X, Y position on cylinder surface
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            
            points.append((x, y, z))
        
        # Create a cutting shape from these points
        if len(points) > 2:
            # Create a V-groove by making a thin wedge
            cutting_width = groove_depth
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                
                # Create a small cutting geometry at this location
                if i % 3 == 0:  # Sample to reduce complexity
                    try:
                        cut_shape = (cq.Workplane("XY")
                                   .moveTo(p1[0], p1[1])
                                   .circle(groove_depth/2)
                                   .extrude(pitch/4, both=True)
                                   .translate((0, 0, p1[2])))
                        result = result.cut(cut_shape)
                    except:
                        pass

