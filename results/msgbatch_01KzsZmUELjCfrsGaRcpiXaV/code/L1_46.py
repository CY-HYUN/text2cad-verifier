import cadquery as cq

# Create a right-angled triangular prism
# Base: right-angled triangle with sides 30mm (X) and 40mm (Y)
# Height: 60mm (Z)

# Create the triangular base by drawing the triangle vertices
base = cq.Workplane("XY").moveTo(0, 0).lineTo(30, 0).lineTo(0, 40).close()

# Extrude the triangle along the Z-axis by 60mm
result = base.extrude(60)
