import cadquery as cq

# Create a cube with edge length 50mm, centered at the origin
cube = cq.Workplane("XY").box(50, 50, 50)

# Cut a circular hole through the center along the Z-axis
# The hole has a diameter of 20mm (radius 10mm) and goes through the entire height
result = cube.faces(">Z").workplane().hole(20)
