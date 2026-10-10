import cadquery as cq
import math

# Define the cubic Bézier curve function
def bezier_cubic(t, p0, p1, p2, p3):
    """Cubic Bézier curve: B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3"""
    mt = 1 - t
    mt3 = mt ** 3
    mt2 = mt ** 2
    t2 = t ** 2
    t3 = t ** 3
    
    x = mt3 * p0[0] + 3 * mt2 * t * p1[0] + 3 * mt * t2 * p2[0] + t3 * p3[0]
    y = mt3 * p0[1] + 3 * mt2 * t * p1[1] + 3 * mt * t2 * p2[1] + t3 * p3[1]
    z = mt3 * p0[2] + 3 * mt2 * t * p1[2] + 3 * mt * t2 * p2[2] + t3 * p3[2]
    
    return (x, y, z)

def bezier_tangent(t, p0, p1, p2, p3):
    """Derivative of cubic Bézier curve for local orientation"""
    mt = 1 - t
    mt2 = mt ** 2
    t2 = t ** 2
    
    dx = 3 * mt2 * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0]) + 3 * t2 * (p3[0] - p2[0])
    dy = 3 * mt2 * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1]) + 3 * t2 * (p3[1] - p2[1])
    dz = 3 * mt2 * (p1[2] - p0[2]) + 6 * mt * t * (p2[2] - p1[2]) + 3 * t2 * (p3[2] - p2[2])
    
    mag = math.sqrt(dx**2 + dy**2 + dz**2)
    if mag < 1e-6:
        return (0, 0, 1)
    return (dx/mag, dy/mag, dz/mag)

# Bézier curve control points
p0 = (0, 0, 0)
p1 = (0, 0, 60)
p2 = (60, 0, 60)
p3 = (60, 0, 120)

# Generate loft sections
num_sections = 20
sections = []

for i in range(num_sections + 1):
    t = i / num_sections
    
    # Get point on Bézier curve
    center = bezier_cubic(t, p0, p1, p2, p3)
    tangent = bezier_tangent(t, p0, p1, p2, p3)
    
    # Interpolate between ellipse (at t=0) and circle (at t=1)
    # At bottom: ellipse with semi-major axis a=60, semi-minor axis b=40
    # At top: circle with radius=30
    a = 60 * (1 - t) + 30 * t
    b = 40 * (1 - t) + 30 * t
    
    # Create profile points for this section
    num_points = 32
    profile_points = []
    
    for j in range(num_points):
        angle = 2 * math.pi * j / num_points
        
        # Ellipse/circle profile in local coordinates
        x_local = a * math.cos(angle)
        y_local = b * math.sin(angle)
        z_local = 0
        
        # For top section, rotate to match 45-degree tilt
        if t > 0.99:
            # Top circle at 45-degree tilt
            cos45 = math.cos(math.pi / 4)
            sin45 = math.sin(math.pi / 4)
            z_rot = z_local * cos45 - x_local * sin45
            x_rot = z_local * sin45 + x_local * cos45
            x_local = x_rot
            z_local = z_rot
        
        # Transform to 3D position using local frame
        # Create orthonormal frame with tangent as Z-axis
        if abs(tangent[2]) < 0.99:
            right = (tangent[1], -tangent[0], 0)
        else:
            right = (1, 0, 0)
        
        mag = math.sqrt(right[0]**2 + right[1]**2 + right[2]**2)
        if mag > 1e-6:
            right = (right[0]/mag, right[1]/mag, right[2]/mag)
        
        up = (tangent[1]*0 - tangent[2]*right[1], 
              tangent[2]*right[0] - tangent[0]*0,
              tangent[0]*right[1] - tangent[1]*right[0])
        mag = math.sqrt(up[0]**2 + up[1]**2 + up[2]**2)
        if mag > 1e-6:
            up = (up[0]/mag, up[1]/mag, up[2]/mag)
        
        x_world = center[0] + x_local * right[0] + y_local * up[0]
        y_world = center[1] + x_local * right[1] + y_local * up[1]
        z_world = center[2] + x_local * right[2] + y_local * up[2]
        
        profile_points.append((x_world, y_world, z_world))
    
    sections.append(profile_points)

# Create outer loft
outer_wires = []
for section in sections:
    wire = cq.Workplane("XY").polyline(section + [section[0]]).wire()
    outer_wires.append(wire)

outer_solid = cq.Workplane("XY").loft(*outer_wires)

# Create inner loft (subtract for hollow structure with 3mm wall thickness)
inner_sections = []
for section in sections:
    inner_profile = []
    for pt in section:
        # Move inward by 3mm along local normal (simplified radial reduction)
        center_x = sum(p[0] for p in section) / len(section)
        center_y = sum(p[1] for p in section) / len(section)
        center_z = sum(p[2] for p in section) / len(section)
        
        dx = pt[0] - center_x
        dy = pt[1] - center_y
        dz = pt[2] - center_z
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        
        if dist > 1e-6:
            factor = (dist - 3) / dist
            new_x = center_x + dx * factor
            new_y = center_y + dy * factor
            new_z = center_z + dz * factor
            inner_profile.append((new_x, new_y, new_z))
        else:
            inner_profile.append(pt)
    
    inner_sections.append(inner_profile)

inner_wires = []
for section in inner_sections:
    wire = cq.Workplane("XY").polyline(section + [section[0]]).wire()
    inner_wires.append(wire)

inner_solid = cq.Workplane("XY").loft(*inner_wires)

# Create hollow manifold
result = outer_solid.cut(inner_solid)
