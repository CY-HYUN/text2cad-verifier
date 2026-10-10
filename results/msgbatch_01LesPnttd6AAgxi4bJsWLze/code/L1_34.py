import cadquery as cq

# Create the base rectangular prism (60mm wide, 20mm high, 100mm long)
base = cq.Workplane("XY").box(100, 60, 20)

# Create the top rectangular prism (30mm wide, 20mm high, 100mm long)
# Positioned on top of the base, centered in the Y direction
top = cq.Workplane("XY").box(100, 30, 20).translate((0, 0, 20))

# Combine both prisms
result = base.union(top)
