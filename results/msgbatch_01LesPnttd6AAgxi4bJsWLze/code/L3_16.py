import cadquery as cq
import math

# Create a streamlined ergonomic mouse top cover

# Define the longitudinal spine (side profile) using cubic Bezier curve
def bezier_curve_3d(p0, p1, p2, p3, t):
    """Evaluate cubic Bezier curve at parameter t (0 to 1)"""
    mt = 1 - t
    return (
        mt**3 * p0[0] + 3*mt**2*t * p1[0] + 3*mt*t**2 * p2[0] + t**3 * p3[0],
        mt**3 * p0[1] + 3*mt**2*t * p1[1] + 3*mt*t**2 * p2[1] + t**3 * p3[1],
        mt**3 * p0[2] + 3*mt**2*t * p1[2] + 3*mt*t**2 * p2[2] + t**3 * p3[2]
    )

# Longitudinal spine control points
p0_spine = (0, 0, 0)
p1_spine = (20, 0, 35)
p2_spine = (80, 0, 35)
p3_spine = (110, 0, 0)

# Generate spine curve
spine_points = []
for i in range(51):
    t = i / 50.0
    pt = bezier_curve_3d(p0_spine, p1_spine, p2_spine, p3_spine, t)
    spine_points.append(pt)

# Create transverse profiles at different longitudinal positions
def get_profile_width(x):
    """Width varies with position, widest at rear third (around x=37)"""
    # Maximum width at x ≈ 37 (rear third of 110mm length)
    width = 30 + 30 * math.exp(-((x - 37)**2) / 400)
    return width

def get_profile_height(x):
    """Height based on spine curve"""
    t = x / 110.0
    _, _, z = bezier_curve_3d(p0_spine, p1_spine, p2_spine, p3_spine, t)
    return z

# Generate lofting profiles
profiles = []
for i in range(51):
    x = i * 110 / 50.0
    z_spine = get_profile_height(x)
    width = get_profile_width(x)
    
    # Create profile points (cross-section)
    profile_pts = []
    for j in range(21):
        angle = j * math.pi / 20.0  # Half circle from left to right
        y = -width/2 * math.cos(angle)
        z = z_spine * math.sin(angle) ** 0.5  # Smooth curve inward
        profile_pts.append((x, y, z))
    
    profiles.append(profile_pts)

# Build the surface using lofting
workplane = cq.Workplane("XY")

# Create wires from profiles
wires = []
for profile in profiles:
    wire_pts = [cq.Vector(*pt) for pt in profile]
    wire = cq.Workplane("XY").polyline(wire_pts).close().wire()
    wires.append(wire)

# Loft between wires
result = cq.Workplane("XY").loft(wires, ruled=False)

# Add thickness by creating a shell
result = result.shell(1.5)

# Create thumb rest depression on the left side
# Thumb rest is a concave surface trimmed from left side, around x=40-70 range
thumb_rest = cq.Workplane("XY").sphere(35).translate((55, -45, 15))

# Combine with boolean cut to create thumb rest
try:
    result = result.cut(thumb_rest)
except:
    pass

# Ensure smooth result
result = result.clean()

