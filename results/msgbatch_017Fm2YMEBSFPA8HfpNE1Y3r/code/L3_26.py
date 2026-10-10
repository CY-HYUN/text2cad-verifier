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
        radius = max_radius - (max_radius - min_radius) * (1 - math.cos(progress * math.pi)) / 2
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))
    
    # 90-degree return segment (0 to 90 degrees) using modified sine
    for angle in range(0, 91, 5):
        progress = angle / 90.0
        radius = min_radius + (max_radius - min_radius) * (1 - math.cos(progress * math.pi)) / 2
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))
    
    return points

# Create main cam using polygon extrusion
main_cam_points = create_main_cam_profile()
main_cam = cq.Workplane("XY").polyline(main_cam_points).close().extrude(15.0)

# Create conjugate cam at Z = 35.0 (net spacing of 20.0 mm)
min_radius = 50.0
max_radius = 90.0
offset = 10.0

conjugate_points = []

# 180-degree dwell arc at min radius
for angle in range(90, 271, 5):
    rad = math.radians(angle)
    x = (min_radius - offset) * math.cos(rad)
    y = (min_radius - offset) * math.sin(rad)
    conjugate_points.append((x, y))

# 90-degree return segment
for angle in range(270, 361, 5):
    progress = (angle - 270) / 90.0
    radius = (min_radius - offset) + offset * (1 - math.cos(progress * math.pi)) / 2
    rad = math.radians(angle)
    x = radius * math.cos(rad)
    y = radius * math.sin(rad)
    conjugate_points.append((x, y))

# 90-degree rise segment
for angle in range(0, 91, 5):
    progress = angle / 90.0
    radius = (max_radius - offset) - offset * (1 - math.cos(progress * math.pi)) / 2
    rad = math.radians(angle)
    x = radius * math.cos(rad)
    y = radius * math.sin(rad)
    conjugate_points.append((x, y))

conjugate_cam = cq.Workplane("XY").transformed(offset=cq.Vector(0, 0, 35.0)).polyline(conjugate_points).close().extrude(15.0)

# Combine both cams
assembly = main_cam.union(conjugate_cam)

# Create through-hole for shaft (25.0 mm diameter) - extended length
hole = cq.Workplane("XY").circle(12.5).extrude(60.0, both=True)

# Create keyway feature (6.0 mm width and depth)
keyway = cq.Workplane("XY").box(6.0, 6.0, 60.0, centered=True)

# Cut hole and keyway from assembly
assembly = assembly.cut(hole)
assembly = assembly.cut(keyway)

# Apply chamfer to outer edges
try:
    assembly = assembly.chamfer(1.0)
except:
    # If chamfer fails on all edges, apply selectively
    assembly = assembly.edges("|Z").chamfer(1.0)

result = assembly
