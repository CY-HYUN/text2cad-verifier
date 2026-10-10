import cadquery as cq

# Create the first rectangular prism along the X-axis
# 100mm long (X), 20mm wide (Y), 20mm high (Z)
prism1 = cq.Workplane("XY").box(100, 20, 20)

# Create the second rectangular prism along the Y-axis
# 20mm long (X), 100mm wide (Y), 20mm high (Z)
prism2 = cq.Workplane("XY").box(20, 100, 20)

# Combine both prisms using union to create the cross-beam structure
result = prism1.union(prism2)
