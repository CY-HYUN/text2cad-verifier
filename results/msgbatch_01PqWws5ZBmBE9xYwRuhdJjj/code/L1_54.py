import cadquery as cq

# Create a sphere centered at (0, 0, 0) with radius 25.0
sphere = cq.Workplane("XY").sphere(25.0)

# Create a cutting cylinder with axis along Z-axis, radius 7.0, height 60.0
# The cylinder is centered at origin by default
cylinder = cq.Workplane("XY").cylinder(height=60.0, radius=7.0)

# Perform Boolean difference: sphere - cylinder
result = sphere.cut(cylinder)
