import cadquery as cq
import math

# Create the lower cylindrical flange
outer_diameter = 200
flange_height = 50
wall_thickness = 10
inner_diameter = outer_diameter - 2 * wall_thickness

# Create the lower cylindrical flange
lower_flange = cq.Workplane("XY").cylinder(
    height=flange_height, 
    radius=outer_diameter/2, 
    centered=False
)

# Create the inner hole in the flange
lower_flange = lower_flange.faces(">Z").workplane().hole(inner_diameter)

# Create the ellipsoidal dome
# Major axis (a) = 100 mm (radius in XY plane)
# Minor axis (b) = 100 mm (depth along height)
# The ellipsoid equation: (x²/a² + y²/a² + z²/b²) = 1
a = outer_diameter / 2  # 100 mm
b = 100  # depth of the ellipsoid (semi-minor axis in Z)

# Create the outer ellipsoid
outer_ellipsoid = cq.Workplane("XY").ellipsoid(
    x_radius=a, 
    y_radius=a, 
    z_radius=b, 
    centered=True
)

# Translate it up so it sits on top of the flange
outer_ellipsoid = outer_ellipsoid.translate((0, 0, flange_height + b))

# Create inner ellipsoid for wall thickness (subtract to create hollow)
inner_a = a - wall_thickness
inner_b = b - wall_thickness

inner_ellipsoid = cq.Workplane("XY").ellipsoid(
    x_radius=inner_a, 
    y_radius=inner_a, 
    z_radius=inner_b, 
    centered=True
)

inner_ellipsoid = inner_ellipsoid.translate((0, 0, flange_height + inner_b))

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
