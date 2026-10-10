import cadquery as cq
import math

# Create the lower cylindrical flange
outer_diameter = 200
flange_height = 50
wall_thickness = 10
inner_diameter = outer_diameter - 2 * wall_thickness

# Create the lower cylindrical flange (outer cylinder)
lower_flange = cq.Workplane("XY").cylinder(
    height=flange_height, 
    radius=outer_diameter/2, 
    centered=False
)

# Create the inner hole in the flange
lower_flange = lower_flange.faces(">Z").workplane().hole(inner_diameter)

# Create the ellipsoidal dome using a solid approach
# Major axis (a) = 100 mm (radius in XY plane)
# Minor axis (b) = 100 mm (depth along height)
a = outer_diameter / 2  # 100 mm
b = 100  # depth of the ellipsoid (semi-minor axis in Z)

# Create outer ellipsoid by revolving an ellipse profile
def create_ellipsoid(a_rad, b_rad, z_offset):
    # Create ellipse profile in XZ plane
    points = []
    steps = 100
    for i in range(steps + 1):
        angle = math.pi * i / steps
        x = a_rad * math.cos(angle)
        z = b_rad * math.sin(angle)
        points.append((x, z))
    
    # Revolve around Z axis
    profile = cq.Workplane("XZ").polyline(points)
    solid = profile.revolve(360, (0, 0, 0), (0, 0, 1))
    return solid.translate((0, 0, z_offset))

# Create outer ellipsoid dome
outer_ellipsoid = create_ellipsoid(a, b, flange_height)

# Create inner ellipsoid for wall thickness
inner_a = a - wall_thickness
inner_b = b - wall_thickness
inner_ellipsoid = create_ellipsoid(inner_a, inner_b, flange_height)

# Create the dome by subtracting the inner ellipsoid from the outer
dome = outer_ellipsoid.cut(inner_ellipsoid)

# Combine lower flange and dome
vessel_head = lower_flange.union(dome)

# Create the nozzle flange at the apex
nozzle_outer_diameter = 40
nozzle_inner_diameter = 30
nozzle_height = 30

nozzle_flange = cq.Workplane("XY").cylinder(
    height=nozzle_height, 
    radius=nozzle_outer_diameter/2, 
    centered=False
)

# Position the nozzle at the apex of the ellipsoid
apex_height = flange_height + b
nozzle_flange = nozzle_flange.translate((0, 0, apex_height))

# Create the hole in the nozzle
nozzle_flange = nozzle_flange.faces(">Z").workplane().hole(nozzle_inner_diameter)

# Combine all parts
result = vessel_head.union(nozzle_flange)
