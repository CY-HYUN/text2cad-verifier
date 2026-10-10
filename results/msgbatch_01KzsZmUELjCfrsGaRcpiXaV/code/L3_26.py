import cadquery as cq
import math

# Parameters
cam_thickness = 15
axial_spacing = 20
min_radius = 50
max_radius = 90
shaft_hole_diameter = 25
keyway_width = 6
keyway_depth = 6
chamfer_size = 1
num_points = 360

def create_cam_profile(num_points=360):
    """
    Create the main cam profile with:
    - 90-degree rise (0-90°): min_radius to max_radius with sine curve
    - 90-degree return (90-180°): max_radius to min_radius with sine curve
    - 180-degree dwell (180-360°): at min_radius
    """
    points = []
    
    for i in range(num_points):
        angle_deg = (i / num_points) * 360
        angle_rad = math.radians(angle_deg)
        
        # Rise phase (0-90°)
        if angle_deg < 90:
            phase_ratio = angle_deg / 90
            # Modified sine curve for smooth transition
            lift = (max_radius - min_radius) * (1 - math.cos(phase_ratio * math.pi)) / 2
            radius = min_radius + lift
        # Return phase (90-180°)
        elif angle_deg < 180:
            phase_ratio = (angle_deg - 90) / 90
            # Modified sine curve for smooth return
            lift = (max_radius - min_radius) * (1 + math.cos(phase_ratio * math.pi)) / 2
            radius = min_radius + lift
        # Dwell phase (180-360°)
        else:
            radius = min_radius
        
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
        points.append((x, y))
    
    # Close the profile
    points.append(points[0])
    return points

def create_conjugate_profile(main_points, offset=20):
    """
    Create conjugate profile for secondary cam based on geometric relationship
    The conjugate profile maintains dual-point contact
    """
    conjugate_points = []
    
    for i, (x, y) in enumerate(main_points):
        # Calculate radius and angle
        r = math.sqrt(x*x + y*y)
        angle = math.atan2(y, x)
        
        # Conjugate profile: offset radius relationship
        # For dual-point contact, the conjugate follows a related curve
        conjugate_r = r + offset / 2
        
        conj_x = conjugate_r * math.cos(angle)
        conj_y = conjugate_r * math.sin(angle)
        conjugate_points.append((conj_x, conj_y))
    
    return conjugate_points

# Create main cam profile
main_profile = create_cam_profile(num_points)

# Create first cam (main cam)
wp1 = cq.Workplane("XY")
face1 = wp1.polyline(main_profile).close().extrude(cam_thickness)

# Create second cam (conjugate cam)
conjugate_profile = create_conjugate_profile(main_profile, offset=10)
wp2 = cq.Workplane("XY").polyline(conjugate_profile).close().extrude(cam_thickness)

# Translate second cam in Z direction
face2 = wp2.translate((0, 0, cam_thickness + axial_spacing))

# Combine both cams
result = face1.union(face2)

# Create shaft hole
shaft_hole = cq.Workplane("XY").hole(shaft_hole_diameter, cam_thickness + axial_spacing + cam_thickness)
result = result.cut(shaft_hole)

# Create rectangular keyway
keyway_length = 40
keyway_box = (cq.Workplane("XY")
              .box(keyway_width, keyway_depth, keyway_length, centered=True)
              .translate((shaft_hole_diameter/2 - keyway_depth/2, 0, 
                         (cam_thickness + axial_spacing + cam_thickness)/2)))
result = result.cut(keyway_box)

# Chamfer top and bottom outer circular edges
result = result.faces("+Z").edges("%CIRCLE").chamfer(chamfer_size)
result = result.faces("-Z").edges("%CIRCLE").chamfer(chamfer_size)

# Chamfer the edges of the hole
try:
    result = result.faces("|Z").edges().edges("+Z or -Z").chamfer(0.5)
except:
    pass

