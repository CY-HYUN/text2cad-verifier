import cadquery as cq
import math

# Create a sphere with diameter 50mm (radius 25mm)
sphere = cq.Workplane("XY").sphere(25)

# Create four cylinders (30mm diameter, 20mm length) along positive/negative X and Y axes
cylinder_radius = 15
cylinder_length = 20

# Cylinder along positive X
cyl_x_pos = cq.Workplane("YZ").circle(cylinder_radius).extrude(cylinder_length).translate((25, 0, 0))

# Cylinder along negative X
cyl_x_neg = cq.Workplane("YZ").circle(cylinder_radius).extrude(cylinder_length).translate((-25, 0, 0))

# Cylinder along positive Y
cyl_y_pos = cq.Workplane("XZ").circle(cylinder_radius).extrude(cylinder_length).translate((0, 25, 0))

# Cylinder along negative Y
cyl_y_neg = cq.Workplane("XZ").circle(cylinder_radius).extrude(cylinder_length).translate((0, -25, 0))

# Combine sphere with all cylinders
result = sphere.union(cyl_x_pos).union(cyl_x_neg).union(cyl_y_pos).union(cyl_y_neg)

# Create cutting cylinders along X and Y axes (20mm diameter, full length cut)
# These create the internal connections
cut_x = cq.Workplane("YZ").circle(10).extrude(150).translate((0, 0, 0))
cut_y = cq.Workplane("XZ").circle(10).extrude(150).translate((0, 0, 0))

# Perform the cuts to connect interior
result = result.cut(cut_x).cut(cut_y)

# Create a circular platform at the top by cutting away material
# The platform has 20mm diameter at the top
platform_cutter = cq.Workplane("XY").circle(10).extrude(10).translate((0, 0, 25))
result = result.cut(platform_cutter)
