import cadquery as cq
import math

# Start with a cylinder base
base_radius = 40  # 80mm diameter
base_height = 60

# Create the base cylinder
base = cq.Workplane("XY").cylinder(base_height, base_radius)

# Create the inclined cut plane
# The plane cuts at 30 degrees, with highest point in negative Y direction
# This creates an elliptical cross-section on top
# The plane normal lies in YZ plane at 30 degrees from horizontal
cut_angle = 30  # degrees
cut_angle_rad = math.radians(cut_angle)

# Create a large box to cut with, positioned to cut the top at 30 degrees
# The cutting plane passes through the center and tilts around X-axis
# Move up by base_height/2, then create cutting geometry
cut_height = 200
cut_box = cq.Workplane("XY").box(200, 200, cut_height).translate((0, -cut_height/2 * math.sin(cut_angle_rad), base_height/2 - cut_height/2 * math.cos(cut_angle_rad)))

# Apply the inclined cut
part = base.cut(cut_box)

# Now create the paraboloid recessed into the inclined surface
# The paraboloid has equation x^2 + y^2 = 40z in local coordinates
# Focal length f = 10mm, opening diameter = 60mm (radius = 30mm)
# Create a paraboloid by revolving a parabola
# For paraboloid: z = (x^2 + y^2) / 40, with max radius 30mm

# Create the paraboloid by building it with a parabolic profile
paraboloid_radius = 30
paraboloid_depth = (paraboloid_radius ** 2) / 40

# Create paraboloid using a 2D parabola revolved around Z
parabola_profile = cq.Workplane("XZ").spline(
    [(i/100 * paraboloid_radius, (i/100 * paraboloid_radius)**2 / 40) for i in range(101)],
    includeCurrent=False
)
paraboloid = parabola_profile.revolve(360, (0, 0, 0), (0, 0, 1))

# Position and orient the paraboloid to sit on the inclined surface
# The vertex is at the center of the inclined elliptical surface
# The axis is perpendicular to the inclined surface
# Transform the paraboloid to align with the inclined surface
paraboloid_positioned = paraboloid.rotate((0, 0, 0), (1, 0, 0), cut_angle)
paraboloid_positioned = paraboloid_positioned.translate((0, base_height/2 * math.sin(cut_angle_rad), base_height/2 - paraboloid_depth/2))

# Cut the paraboloid into the top surface
part = part.cut(paraboloid_positioned)

# Create the sine wave groove on the outer cylindrical surface at Z = 30mm
# 6 complete cycles, amplitude 5mm, semicircular cross-section with radius 2mm
groove_height_z = 30
num_cycles = 6
amplitude = 5
groove_radius = 2

# Create sine wave path in cylindrical coordinates
points = []
num_points = 300
for i in range(num_points + 1):
    theta = (i / num_points) * 2 * math.pi * num_cycles
    # Radial oscillation: base_radius + amplitude * sin(theta)
    r = base_radius + amplitude * math.sin(theta)
    x = r * math.cos(theta * num_cycles / (2 * math.pi * num_cycles))
    y = r * math.sin(theta * num_cycles / (2 * math.pi * num_cycles))
    z = groove_height_z
    points.append((x, y, z))

# Create a circular cross-section for the groove and sweep it along the path
# Use a 2D circle in the plane perpendicular to the path
groove_profile = cq.Workplane("XY").circle(groove_radius)

# Create groove by sweeping a semicircular profile
# For simplicity, we'll create the groove as a series of positioned cylinders
groove_cut = None
for i in range(len(points) - 1):
    p1 = points[i]
    p2 = points[i + 1]
    
    # Create a small cylinder segment
    segment = cq.Workplane("XY").cylinder(groove_radius * 2, groove_radius, centered=True)
    
    # Position at midpoint
    mid_x = (p1[0] + p2[0]) / 2
    mid_y = (p1[1] + p2[1]) / 2
    mid_z = p1[2]
    
    segment = segment.translate((mid_x, mid_y, mid_z))
    
    if groove_cut is None:
        groove_cut = segment
    else:
        groove_cut = groove_cut.union(segment)

# Subtract the groove
if groove_cut is not None:
    part = part.cut(groove_cut)

result = part
