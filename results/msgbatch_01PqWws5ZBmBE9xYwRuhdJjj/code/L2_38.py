import cadquery as cq
import math

# Create the first cylinder along X-axis with diameter 50mm and length 120mm
cyl_x = cq.Workplane("YZ").circle(25).extrude(120, both=True)

# Create the second cylinder along Z-axis with diameter 50mm and length 80mm
cyl_z = cq.Workplane("XY").circle(25).extrude(80, both=True)

# Perform Boolean union
union_result = cyl_x.union(cyl_z)

# Now we need to create the internal cavity
# The internal cavity is a cross-shaped tube with 40mm diameter holes
# We'll create cylinders with 20mm radius (40mm diameter) along both axes

# Create internal cavity cylinder along X-axis (from -60 to 60, total 120mm)
cavity_x = cq.Workplane("YZ").circle(20).extrude(120, both=True)

# Create internal cavity cylinder along Z-axis (from -40 to 40, total 80mm)
cavity_z = cq.Workplane("XY").circle(20).extrude(80, both=True)

# Union the two cavity cylinders to create connected internal cavity
cavity_union = cavity_x.union(cavity_z)

# Perform the cut operation to create the hollow cross-shaped tube
result = union_result.cut(cavity_union)
