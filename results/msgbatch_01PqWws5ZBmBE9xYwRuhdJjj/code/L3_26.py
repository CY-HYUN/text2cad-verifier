import cadquery as cq
import math

def create_main_cam_profile():
    """Create the main cam profile with dwell, rise, and return segments"""
    points = []
    min_radius = 50.0
    max_radius = 90.0
    
    # 180-degree dwell arc at max radius (90 to 270 degrees)
    for angle in range(90, 271, 5):
        rad = math.radians(angle)
        x = max_radius * math.cos(rad)
        y = max_radius * math.sin(rad)
        points.append((x, y))
    
    # 90-degree rise segment (270 to 360 degrees) using modified sine
    for angle in range(270, 361, 5):
        progress = (angle - 270) / 90.0
        # Modified sine curve for smooth rise
        radius = max_radius - (max_radius - min_radius) * (1 - math.cos(progress * math.pi)) / 2
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))
    
    # 90-degree return segment (0 to 90 degrees) using modified sine
    for angle in range(0, 91, 5):
        progress = angle / 90.0
        # Modified sine curve for smooth return
        radius = min_radius + (max_radius - min_radius) * (1 - math.cos(progress * math.pi)) / 2
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))
    
    return points

def create_conjugate_cam_profile():
    """Create the conjugate cam profile based on two-point contact kinematics"""
    points = []
    min_radius = 50.0
    max_radius = 90.0
    
    # Conjugate profile is offset inward from main profile
    offset = 10.0  # Two-point contact offset
    
    # 180-degree dwell arc at min radius (90 to 270 degrees)
    for angle in range(90, 271, 5):
        rad = math.radians(angle)
        x = (min_radius - offset) * math.cos(rad)
        y = (min_radius - offset) * math.sin(rad)
        points.append((x, y))
    
    # 90-degree return segment (270 to 360 degrees) using modified sine
    for angle in range(270, 361, 5):
        progress = (angle - 270) / 90.0
        radius = (min_radius - offset) + (offset) * (1 - math.cos(progress * math.pi)) / 2
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))
    
    # 90-degree rise segment (0 to 90 degrees) using modified sine
    for angle in range(0, 91, 5):
        progress = angle / 90.0
        radius = (max_radius - offset) - (offset) * (1 - math.cos(progress * math.pi)) / 2
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))
    
    return points

# Create main cam
main_cam_points = create_main_cam_profile()
main_cam = cq.Workplane("XY").moveTo(0, 0)

# Create closed contour for main cam
for i, (x, y) in enumerate(main_cam_points):
    if i == 0:
        main_cam = main_cam.moveTo(x, y)
    else:
        main_cam = main_cam.lineTo(x, y)
main_cam = main_cam.close().extrude(15.0)

# Create conjugate cam at Z = 35.0 (net spacing of 20.0 mm = 35.0 - 15.0)
conjugate_cam_points = create_conjugate_cam_profile()
conjugate_cam = cq.Workplane("XY").moveTo(0, 0).transformed(offset=cq.Vector(0, 0, 35.0))

for i, (x, y) in enumerate(conjugate_cam_points):
    if i == 0:
        conjugate_cam = conjugate_cam.moveTo(x, y)
    else:
        conjugate_cam = conjugate_cam.lineTo(x, y)
conjugate_cam = conjugate_cam.close().extrude(15.0)

# Combine both cams
assembly = main_cam.union(conjugate_cam)

# Create through-hole for shaft (25.0 mm diameter)
hole = cq.Workplane("XY").circle(12.5).extrude(50.0, both=True)

# Create keyway feature (6.0 mm width and depth)
keyway = cq.Workplane("XY").transformed(offset=cq.Vector(12.5, 0, 0)).box(6.0, 6.0, 50.0, centered=True)

# Cut hole and keyway
assembly = assembly.cut(hole).cut(keyway)

# Apply 1.0 mm chamfer to all edges
assembly = assembly.chamfer(1.0)

result = assembly
