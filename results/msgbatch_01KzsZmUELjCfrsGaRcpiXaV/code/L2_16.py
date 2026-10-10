import cadquery as cq
import math

# Create the main sphere (50mm diameter, so 25mm radius)
sphere = cq.Workplane("XY").sphere(25)

# Create four cylindrical nozzles in the cross direction
# Each nozzle: 30mm diameter (15mm radius), 20mm length
# Nozzles should extend from the sphere surface
nozzles = []

# +X direction nozzle (extends 20mm in +X from center)
nozzle_x_pos = cq.Workplane("XY").cylinder(20, 15, centered=True).translate((35, 0, 0))
nozzles.append(nozzle_x_pos)

# -X direction nozzle (extends 20mm in -X from center)
nozzle_x_neg = cq.Workplane("XY").cylinder(20, 15, centered=True).translate((-35, 0, 0))
nozzles.append(nozzle_x_neg)

# +Y direction nozzle (extends 20mm in +Y from center)
nozzle_y_pos = cq.Workplane("XY").cylinder(20, 15, centered=True).translate((0, 35, 0))
nozzles.append(nozzle_y_pos)

# -Y direction nozzle (extends 20mm in -Y from center)
nozzle_y_neg = cq.Workplane("XY").cylinder(20, 15, centered=True).translate((0, -35, 0))
nozzles.append(nozzle_y_neg)

# Combine sphere and nozzles
result = sphere
for nozzle in nozzles:
    result = result.union(nozzle)

# Create through-holes along X-axis (20mm diameter = 10mm radius)
hole_x = cq.Workplane("YZ").circle(10).extrude(100, both=True)

# Create through-holes along Y-axis (20mm diameter = 10mm radius)
hole_y = cq.Workplane("XZ").circle(10).extrude(100, both=True)

# Subtract the holes from the main body
result = result.cut(hole_x)
result = result.cut(hole_y)

# Cut a 20mm diameter flat surface from the top of the sphere
# Create a cylindrical cut from the top (10mm radius for 20mm diameter)
flat_cut = cq.Workplane("XY").cylinder(10, 10, centered=True).translate((0, 0, 25))
result = result.cut(flat_cut)
