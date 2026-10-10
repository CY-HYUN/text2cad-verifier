import cadquery as cq
import math

# Create the first cylinder along X-axis with diameter 50mm and length 120mm
# Centered at origin, so it extends from -60 to +60 along X
cyl_x = cq.Workplane("YZ").circle(25).extrude(120, both=True)

# Create the second cylinder along Z-axis with diameter 50mm and length 80mm
# Centered at origin, so it extends from -40 to +40 along Z
cyl_z = cq.Workplane("XY").circle(25).extrude(80, both=True)

# Perform Boolean union
union_result = cyl_x.union(cyl_z)

# Create internal cavity cylinder along X-axis (diameter 40mm, so radius 20mm)
cavity_x = cq.Workplane("YZ").circle(20).extrude(120, both=True)

# Create internal cavity cylinder along Z-axis (diameter 40mm, so radius 20mm)
cavity_z = cq.Workplane("XY").circle(20).extrude(80, both=True)

# Union the two cavity cylinders to create connected internal cavity
cavity_union = cavity_x.union(cavity_z)

# Perform the cut operation to create the hollow cross-shaped tube
result = union_result.cut(cavity_union)
