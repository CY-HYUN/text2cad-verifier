import cadquery as cq

# Create the main flat cylinder body
# Diameter: 100mm, Thickness (Z-direction): 5mm
outer_radius = 50  # 100mm diameter / 2
thickness = 5

# Create a solid cylinder
cylinder = cq.Workplane("XY").cylinder(height=thickness, radius=outer_radius, centered=True)

# Create the central hole (diameter 50mm)
# The hole is drilled vertically through the entire thickness
hole_radius = 25  # 50mm diameter / 2

# Subtract the hole from the cylinder to create the ring
result = cylinder.faces(">Z").workplane().hole(diameter=hole_radius * 2, depth=thickness)
