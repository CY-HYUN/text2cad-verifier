import cadquery as cq

# Create a 50mm cube
cube = cq.Workplane("XY").box(50, 50, 50)

# Select the front face and cut a hole with diameter 15mm to depth 30mm
cube = cube.faces(">Z").workplane().circle(15/2).cutBlind(-30)

# Select the top face and cut a hole with diameter 15mm to depth 30mm
cube = cube.faces(">Y").workplane().circle(15/2).cutBlind(-30)

result = cube
