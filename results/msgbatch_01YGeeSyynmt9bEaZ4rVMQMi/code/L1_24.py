import cadquery as cq

# Vertical plate: 40 wide (Y) x 60 high (Z), 10 thick along +X
vertical = cq.Workplane("XY").box(10.0, 40.0, 60.0, centered=(False, True, False))

# Horizontal plate: 50 long (X) x 40 wide (Y), 10 thick along +Z
horizontal = cq.Workplane("XY").box(50.0, 40.0, 10.0, centered=(False, True, False))

result = vertical.union(horizontal)
