import cadquery as cq

# Create the rectangular base (40x40x20)
base = cq.Workplane("XY").box(40, 40, 20)

# Create the cylinder (20mm diameter, 20mm height) centered on top
# The cylinder's center will be at z=20 (top of the base)
cylinder = cq.Workplane("XY").workplane(offset=20).cylinder(20, 10)

# Combine the two shapes
result = base.union(cylinder)
