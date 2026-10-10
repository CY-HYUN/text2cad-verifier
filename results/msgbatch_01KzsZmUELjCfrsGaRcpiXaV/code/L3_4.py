import cadquery as cq
import math

def bezier_point(p0, p1, p2, p3, t):
    """Calculate a point on a cubic Bezier curve"""
    mt = 1 - t
    mt2 = mt * mt
    mt3 = mt2 * mt
    t2 = t * t
    t3 = t2 * t
    
    x = mt3*p0[0] + 3*mt2*t*p1[0] + 3*mt*t2*p2[0] + t3*p3[0]
    y = mt3*p0[1] + 3*mt2*t*p1[1] + 3*mt*t2*p2[1] + t3*p3[1]
    z = mt3*p0[2] + 3*mt2*t*p1[2] + 3*mt*t2*p2[2] + t3*p3[2]
    
    return (x, y, z)

def get_cross_section(x_pos, spine_y):
    """Get cross-section shape at given x position"""
    if x_pos <= 0:
        # Circle at start: diameter 15mm
        radius = 7.5
        points = []
        for i in range(32):
            angle = 2 * math.pi * i / 32
            y = radius * math.cos(angle) + spine_y
            z = radius * math.sin(angle)
            points.append((y, z))
        points.append(points[0])
        return points
    elif x_pos <= 50:
        # Transition from circle to ellipse at X=50
        t = x_pos / 50.0
        radius_start = 7.5
        major_50 = 12.5
        minor_50 = 10.0
        
        radius = radius_start * (1 - t) + major_50 * t
        minor = radius_start * (1 - t) + minor_50 * t
        
        points = []
        for i in range(32):
            angle = 2 * math.pi * i / 32
            y = radius * math.cos(angle) + spine_y
            z = minor * math.sin(angle)
            points.append((y, z))
        points.append(points[0])
        return points
    elif x_pos <= 100:
        # Ellipse at X=50: major=25, minor=20
        t = (x_pos - 50) / 50.0
        major_50 = 12.5
        minor_50 = 10.0
        major_100 = 11.0
        minor_100 = 9.0
        
        major = major_50 * (1 - t) + major_100 * t
        minor = minor_50 * (1 - t) + minor_100 * t
        
        points = []
        for i in range(32):
            angle = 2 * math.pi * i / 32
            y = major * math.cos(angle) + spine_y
            z = minor * math.sin(angle)
            points.append((y, z))
        points.append(points[0])
        return points
    elif x_pos <= 150:
        # Transition from ellipse to circle at end
        t = (x_pos - 100) / 50.0
        major_100 = 11.0
        minor_100 = 9.0
        radius_end = 10.0
        
        major = major_100 * (1 - t) + radius_end * t
        minor = minor_100 * (1 - t) + radius_end * t
        
        points = []
        for i in range(32):
            angle = 2 * math.pi * i / 32
            y = major * math.cos(angle) + spine_y
            z = minor * math.sin(angle)
            points.append((y, z))
        points.append(points[0])
        return points
    else:
        # Circle at end: diameter 20mm
        radius = 10.0
        points = []
        for i in range(32):
            angle = 2 * math.pi * i / 32
            y = radius * math.cos(angle) + spine_y
            z = radius * math.sin(angle)
            points.append((y, z))
        points.append(points[0])
        return points

# Bezier control points for spine
p0 = (0, 0, 0)
p1 = (30, 20, 0)
p2 = (100, 25, 0)
p3 = (150, 5, 0)

# Create cross-sections along the spine
sections = []
num_sections = 31

for i in range(num_sections):
    t = i / (num_sections - 1)
    spine_point = bezier_point(p0, p1, p2, p3, t)
    x_pos = spine_point[0]
    spine_y = spine_point[1]
    
    cross_section_points = get_cross_section(x_pos, spine_y)
    
    # Convert 2D points to 3D with x coordinate
    section_3d = [cq.Vector(x_pos, pt[0], pt[1]) for pt in cross_section_points]
    sections.append(section_3d)

# Create lofted surface
section_wires = []
for section_points in sections:
    wire = cq.Wire.makePolygon(section_points)
    section_wires.append(wire)

# Loft through all sections
loft_shell = cq.Shell.makeLoft(section_wires)
outer_solid = cq.Solid.makeSolid(loft_shell)

# Create inner solid by scaling down for shell thickness
wall_thickness = 1.5
scale_factor = 1.0 - (wall_thickness / 12.5)  # Approximate scaling

# Create scaled inner sections
inner_sections = []
for i in range(num_sections):
    t = i / (num_sections - 1)
    spine_point = bezier_point(p0, p1, p2, p3, t)
    x_pos = spine_point[0]
    spine_y = spine_point[1]
    
    cross_section_points = get_cross_section(x_pos, spine_y)
    
    # Scale the cross-section inward
    scaled_points = []
    for pt in cross_section_points:
        scaled_y = (pt[0] - spine_y) * scale_factor + spine_y
        scaled_z = pt[1] * scale_factor
        scaled_points.append((scaled_y, scaled_z))
    
    section_3d = [cq.Vector(x_pos, pt[0], pt[1]) for pt in scaled_points]
    inner_sections.append(section_3d)

inner_wires = []
for section_points in inner_sections:
    wire = cq.Wire.makePolygon(section_points)
    inner_wires.append(wire)

inner_shell = cq.Shell.makeLoft(inner_wires)
inner_solid = cq.Solid.makeSolid(inner_shell)

# Create shell by cutting inner from outer
result = outer_solid.cut(inner_solid)
