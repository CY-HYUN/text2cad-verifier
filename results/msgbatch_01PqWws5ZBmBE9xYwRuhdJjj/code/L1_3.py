import cadquery as cq

# Create a new workplane with origin at (0,0,0) on the XY plane
wp = cq.Workplane("XY")

# Draw a square centered at the origin with side length 50mm
# Using sketch on XY plane
square = wp.sketch().rect(50.0, 50.0).finalize()

# Extrude the square 50mm along the +Z direction to form a cube
cube = square.extrude(50.0)

# Create a sketch on the top face of the cube
top_face = cube.faces(">Z").workplane()

# Draw a circle centered at the origin with diameter 20mm (radius 10mm)
circle = top_face.sketch().circle(10.0).finalize()

# Extrude cut through the entire part (cut down more than 50mm to ensure it goes through)
result = circle.cutBlind(-60.0)
