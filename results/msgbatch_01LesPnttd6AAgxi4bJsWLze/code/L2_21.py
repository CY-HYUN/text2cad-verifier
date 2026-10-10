import cadquery as cq
import math

# Create the base plate
plate = cq.Workplane("XY").box(100, 100, 10, centered=True)

# Create a sphere with diameter 40mm (radius 20mm)
sphere = cq.Workplane("XY").sphere(20)

# Position the sphere so its center is on the upper surface of the plate
# Upper surface of plate is at z = 5 (since plate is 10mm thick and centered at origin)
sphere = sphere.translate((0, 0, 5))

# Union the sphere with the plate to create the embedded sphere effect
result = plate.union(sphere)

# Cut the bottom flat - we need to cut everything below z = -5 (bottom of plate)
# Create a cutting box that extends below the plate
cutting_box = cq.Workplane("XY").box(200, 200, 20, centered=True).translate((0, 0, -15))

# Cut away the bottom portion to create the flat bottom surface
result = result.intersect(cq.Workplane("XY").box(200, 200, 20, centered=True).translate((0, 0, 0)))

# Actually, let's reconsider - we want a flat bottom surface at z = -5
# Create the final part by cutting with a plane at the bottom of the plate
result = plate.union(sphere)

# Cut everything below z = -5 to create flat bottom
result = result.cut(cq.Workplane("XY").box(300, 300, 10, centered=True).translate((0, 0, -15)))
