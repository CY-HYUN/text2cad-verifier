import cadquery as cq
import math

# Start with a cylinder base
base_radius = 40  # 80mm diameter
base_height = 60

# Create the base cylinder
base = cq.Workplane("XY").cylinder(base_height, base_radius)

# Create the inclined cut plane at 30 degrees
cut_angle = 30  # degrees
cut_angle_rad = math.radians(cut_angle)

# Create a cutting box to remove the top at an angle
# The plane cuts the cylinder, highest point in negative Y direction
cut_height = 200
cut_box = cq.Workplane("XY").box(200, 200, cut_height)
cut_box = cut_box.translate((0, -50, 100))

# Rotate the cutting box around X-axis to get 30 degree angle
cut_box = cut_box.rotate((0, 0, 0), (1, 0, 0), -cut_angle)

# Apply the inclined cut
part = base.cut(cut_box)

# Create the paraboloid recessed into the inclined surface
# The paraboloid has equation x^2 + y^2 = 40z
# Focal length f = 10mm, opening diameter = 60mm (radius = 30mm)
paraboloid_radius = 30
paraboloid_depth = (paraboloid_radius ** 2) / 40

# Build paraboloid by creating concentric circles at increasing heights
paraboloid_solid = cq.Workplane("XY")
for i in range(100):
    z_level = i * paraboloid_depth / 100
    r_at_z = math.sqrt(40 * z_level)
    if r_at_z <= paraboloid_radius:
        circle = cq.Workplane("XY").circle(r_at_z).extrude(paraboloid_depth / 100)
        circle = circle.translate((0, 0, z_level))
        if i == 0:
            paraboloid_solid = circle
        else:
            paraboloid_solid = paraboloid_solid.union(circle)

# Position the paraboloid on the inclined surface
paraboloid_positioned = paraboloid_solid.rotate((0, 0, 0), (1, 0, 0), cut_angle)
paraboloid_positioned = paraboloid_positioned.translate((0, -base_height/2 * math.sin(cut_angle_rad), base_height/2 + 5))

# Cut the paraboloid into the part
part = part.cut(paraboloid_positioned)

# Create the sine wave groove on the outer cylindrical surface at Z = 30mm
# 6 complete cycles, amplitude 5mm, semicircular cross-section radius 2mm
groove_height_z = 30
num_cycles = 6
amplitude = 5
groove_radius = 2

# Create sine wave groove as a series of small spheres along the sine path
groove_cut = None
num_points = 360
for i in range(num_points):
    theta = (i / num_points) * 2 * math.pi * num_cycles
    
    # Angle around the cylinder
    circumference_angle = (i / num_points) * 2 * math.pi
    
    # Radial distance from center: base radius + sine wave oscillation
    r = base_radius + amplitude * math.sin(theta)
    
    # Cartesian coordinates
    x = r * math.cos(circumference_angle)
    y = r * math.sin(circumference_angle)
    z = groove_height_z
    
    # Create a small sphere at this point
    sphere = cq.Workplane("XY").sphere(groove_radius).translate((x, y, z))
    
    if groove_cut is None:
        groove_cut = sphere
    else:
        groove_cut = groove_cut.union(sphere)

# Subtract the groove
if groove_cut is not None:
    part = part.cut(groove_cut)

result = part
