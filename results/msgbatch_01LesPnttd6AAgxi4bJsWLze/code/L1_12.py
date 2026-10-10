import cadquery as cq

# Create the main cylinder body
result = cq.Workplane("XY").circle(45).extrude(15)

# Cut the square hole through the center
# The square hole has side length of 30mm, centered at origin
square_size = 30
result = result.faces(">Z").workplane().rect(square_size, square_size).cutThruAll()

