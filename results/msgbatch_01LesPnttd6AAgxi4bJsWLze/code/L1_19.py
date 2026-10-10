import cadquery as cq

# Create the outer cylindrical tube
# Outer diameter: 80mm, Inner diameter: 60mm, Height: 20mm
outer_tube = (
    cq.Workplane("XY")
    .cylinder(height=20, radius=40, centered=True)  # radius = 80/2
    .faces(">Z or <Z").shell(-10)  # shell with thickness to create inner diameter of 60mm
)

# Create the inner cylindrical tube
# Outer diameter: 40mm, Inner diameter: 20mm, Height: 20mm
inner_tube = (
    cq.Workplane("XY")
    .cylinder(height=20, radius=20, centered=True)  # radius = 40/2
    .faces(">Z or <Z").shell(-10)  # shell with thickness to create inner diameter of 20mm
)

# Combine both tubes (they are concentric and independent)
result = outer_tube.union(inner_tube)
