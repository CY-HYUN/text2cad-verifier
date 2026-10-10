import cadquery as cq

# Create the base: a square with side length 60mm, extruded 10mm
base = (
    cq.Workplane("XY")
    .box(60, 60, 10)
)

# Create the cylindrical pillar at the center of the top surface
# The top surface of the base is at z=5 (since base height is 10mm, center is at 5)
# We create a cylinder with diameter 30mm (radius 15mm), extruded 50mm upward from z=5
pillar = (
    cq.Workplane("XY")
    .workplane(offset=5)  # Move to top surface of base
    .circle(15)  # radius = diameter/2 = 30/2 = 15
    .extrude(50)
)

# Combine the base and pillar into a single body
result = base.union(pillar)
