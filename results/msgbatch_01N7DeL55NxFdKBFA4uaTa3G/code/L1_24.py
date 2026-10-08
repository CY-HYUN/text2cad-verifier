import cadquery as cq

# Vertical plate: 40 (Y) x 60 (Z), extruded 10 along +X
vertical = cq.Workplane("XY").box(10.0, 40.0, 60.0, centered=False)

# Horizontal plate: 50 (X) x 40 (Y), extruded 10 along +Z
horizontal = cq.Workplane("XY").box(50.0, 40.0, 10.0, centered=False)

# Union to form L-shaped bracket
result = vertical.union(horizontal)
