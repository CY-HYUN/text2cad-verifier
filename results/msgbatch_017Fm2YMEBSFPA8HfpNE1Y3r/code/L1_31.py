import cadquery as cq
import math

# Create a sphere with radius 25.0 mm centered at origin
sphere = cq.Solid.makeSphere(25.0)

# Create a square column (cutting body)
# Square with side length 20.0 mm on XY plane
# Extrude symmetrically along Z direction with total length 50.0 mm
# This means -25.0 to +25.0 in Z direction

# Create square on XY plane centered at origin
square_column = (
    cq.Workplane("XY")
    .rect(20.0, 20.0)  # 20mm x 20mm square centered at origin
    .extrude(50.0, symmetric=True)  # Extrude 50mm total (25mm up, 25mm down, symmetric)
)

# Perform difference operation: sphere - square_column
result = sphere.cut(square_column.val())
