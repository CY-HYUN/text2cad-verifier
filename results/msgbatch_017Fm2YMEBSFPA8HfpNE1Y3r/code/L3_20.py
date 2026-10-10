import cadquery as cq
import math

# Create the hub: 30mm diameter circle extruded by 20mm
hub = cq.Workplane("XY").circle(15).extrude(20)

# Create root airfoil sketch on a plane 15mm from center
def create_airfoil_profile(chord_length, thickness_ratio=0.12):
    """
    Create a NACA-like airfoil profile using a spline.
    Returns a list of points for the airfoil contour.
    """
    points = []
    num_points = 20
    
    for i in range(num_points + 1):
        x = (i / num_points) * chord_length
        
        # NACA 4-digit style thickness distribution
        t = thickness_ratio
        # Thickness formula
        yt = (t / 0.2) * (0.2969 * math.sqrt(x/chord_length) - 
                          0.1260 * (x/chord_length) - 
                          0.3516 * (x/chord_length)**2 + 
                          0.2843 * (x/chord_length)**3 - 
                          0.1015 * (x/chord_length)**4)
        
        points.append((x, yt))
    
    # Trailing edge
    for i in range(num_points, -1, -1):
        x = (i / num_points) * chord_length
        t = thickness_ratio
        yt = (t / 0.2) * (0.2969 * math.sqrt(x/chord_length) - 
                          0.1260 * (x/chord_length) - 
                          0.3516 * (x/chord_length)**2 + 
                          0.2843 * (x/chord_length)**3 - 
                          0.1015 * (x/chord_length)**4)
        points.append((x, -yt))
    
    return points

# Root airfoil at 15mm radius with 45 degree angle of attack
root_airfoil_points = create_airfoil_profile(25, 0.12)
# Rotate by 45 degrees and translate to root plane
root_angle = math.radians(45)
root_points_rotated = []
for x, y in root_airfoil_points:
    x_rot = x * math.cos(root_angle) - y * math.sin(root_angle)
    y_rot = x * math.sin(root_angle) + y * math.cos(root_angle)
    root_points_rotated.append((x_rot, y_rot, -10))

# Tip airfoil at 75mm radius with 15 degree angle of attack
tip_airfoil_points = create_airfoil_profile(15, 0.12)
# Rotate by 15 degrees and translate to tip plane
tip_angle = math.radians(15)
tip_points_rotated = []
for x, y in tip_airfoil_points:
    x_rot = x * math.cos(tip_angle) - y * math.sin(tip_angle)
    y_rot = x * math.sin(tip_angle) + y * math.cos(tip_angle)
    # Offset to tip plane (75mm from center) and align leading edges
    tip_points_rotated.append((x_rot + 50, y_rot, 10))

# Create root profile as a wire
root_profile_wp = cq.Workplane("XZ").moveTo(root_points_rotated[0][0], root_points_rotated[0][2])
for point in root_points_rotated[1:]:
    root_profile_wp = root_profile_wp.lineTo(point[0], point[2])
root_profile_wire = root_profile_wp.close().val().edges()[0]

# Create tip profile as a wire
tip_profile_wp = cq.Workplane("XZ").moveTo(tip_points_rotated[0][0], tip_points_rotated[0][2])
for point in tip_points_rotated[1:]:
    tip_profile_wp = tip_profile_wp.lineTo(point[0], point[2])
tip_profile_wire = tip_profile_wp.close().val().edges()[0]

# Create blade by lofting between root and tip
blade = cq.Workplane("XY").loft([root_profile_wire, tip_profile_wire])

# Union hub and blade
result = hub.union(blade)

# Apply 2.0mm radius fillet at the connection between blade and hub
result = result.edges("|Z").fillet(2.0)
