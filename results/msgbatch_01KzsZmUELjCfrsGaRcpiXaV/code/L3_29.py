import cadquery as cq
import math

# Parameters
theta_max = 10 * math.pi
num_turns = 5
R_start = 40
R_end = 32.5
pitch = 8
fluctuation_amplitude = 2.5
fluctuation_cycles = 6
rect_width = 8  # width in XY plane
rect_thickness = 1.2  # thickness in Z direction
end_transition = math.pi / 2

# Generate the spring centerline path
def get_point(theta):
    # Radius decreases linearly with theta
    R = R_start - 1.5 * (theta / (2 * math.pi))
    
    # Base Z component (helical rise)
    Z_base = pitch * (theta / (2 * math.pi))
    
    # Fluctuation component with end decay
    if theta > theta_max - end_transition:
        # Linear decay factor approaching the end
        decay = (theta_max - theta) / end_transition
    else:
        decay = 1.0
    
    Z_fluct = fluctuation_amplitude * math.sin(fluctuation_cycles * theta) * decay
    Z = Z_base + Z_fluct
    
    # Cartesian coordinates
    X = R * math.cos(theta)
    Y = R * math.sin(theta)
    
    return (X, Y, Z)

# Generate centerline points
num_points = 400
centerline_points = [get_point(theta_max * i / (num_points - 1)) for i in range(num_points)]

# Create the base wire from centerline points
pts = [cq.Vector(*p) for p in centerline_points]
centerline = cq.Wire.makePolygon(pts)

# Create rectangular cross-section profile
def create_profile_at_theta(theta):
    R = R_start - 1.5 * (theta / (2 * math.pi))
    
    # Radial direction in XY plane
    radial_angle = theta
    
    # Create rectangle centered at origin, oriented perpendicular to radial direction
    # Width (8mm) perpendicular to radial direction (tangential direction in XY)
    # Thickness (1.2mm) in Z direction
    
    # Local coordinate system at this point:
    # - radial direction: (cos(theta), sin(theta), 0)
    # - tangential direction: (-sin(theta), cos(theta), 0)
    # - Z direction: (0, 0, 1)
    
    # Rectangle in local coordinates: width along tangential, thickness along Z
    half_width = rect_width / 2
    half_thickness = rect_thickness / 2
    
    # Corners in local coordinates (tangential, Z)
    local_corners = [
        (-half_width, -half_thickness),
        (half_width, -half_thickness),
        (half_width, half_thickness),
        (-half_width, half_thickness)
    ]
    
    # Transform to global coordinates
    global_corners = []
    for tang_coord, z_coord in local_corners:
        # Tangential direction in global coords
        tang_x = -math.sin(radial_angle)
        tang_y = math.cos(radial_angle)
        
        # Global position
        x = tang_coord * tang_x
        y = tang_coord * tang_y
        z = z_coord
        
        global_corners.append(cq.Vector(x, y, z))
    
    # Create profile wire
    profile = cq.Wire.makePolygon(global_corners)
    return profile

# Create profiles at multiple points along the centerline
num_profiles = 150
profiles = []
thetas = [theta_max * i / (num_profiles - 1) for i in range(num_profiles)]

for i, theta in enumerate(thetas):
    pt = get_point(theta)
    profile = create_profile_at_theta(theta)
    
    # Translate profile to the centerline point
    profile = profile.translate(cq.Vector(pt[0], pt[1], pt[2]))
    profiles.append(profile)

# Create faces by lofting between consecutive profiles
faces = []
for i in range(len(profiles) - 1):
    try:
        lofted = cq.Face.makeLoft([profiles[i], profiles[i + 1]])
        faces.append(lofted)
    except:
        pass

# Create a shell from the faces
if faces:
    shell = cq.Shell.makeShell(faces)
    result = cq.Workplane().add(shell)
else:
    # Fallback: create a simple swept solid
    profile_pts = [cq.Vector(-rect_width/2, -rect_thickness/2, 0),
                   cq.Vector(rect_width/2, -rect_thickness/2, 0),
                   cq.Vector(rect_width/2, rect_thickness/2, 0),
                   cq.Vector(-rect_width/2, rect_thickness/2, 0)]
    profile = cq.Wire.makePolygon(profile_pts)
    result = cq.Workplane().sweep(profile, centerline)

result = cq.Workplane().add(result)
