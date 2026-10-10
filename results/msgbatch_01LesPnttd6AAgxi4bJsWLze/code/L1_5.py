import cadquery as cq

# Create the rectangular base (60mm x 60mm x 10mm)
base = cq.Workplane("XY").box(60, 60, 10, centered=True)

# Create the cylinder (diameter 30mm, height 50mm)
# The cylinder should be centered on top of the base
# Base top surface is at z = 5 (since base height is 10mm, centered at origin means top at z=5)
# Cylinder should start at z = 5 and extend upward to z = 55
cylinder = (
    cq.Workplane("XY")
    .workplane(offset=5)  # Start at the top of the base
    .circle(15)  # radius is 15mm (diameter 30mm)
    .extrude(50)  # height of 50mm
)

# Combine the base and cylinder
result = base.union(cylinder)
