import cadquery as cq
import math

# Create a rectangle (60mm long x 20mm thick) and extrude it 30mm upward
block = cq.Workplane("XY").rect(60.0, 20.0).extrude(30.0)

# Get the front face and create a new workplane on it
front_face = block.faces(">Y").first()
front_wp = cq.Workplane("XY").moveTo(0, 0).transformed(offset=front_face.Center())

# Create a sketch on the front face for the semicircular recess
# The semicircle should be centered at the midpoint of the bottom edge
# On the front face: x ranges from -30 to 30, z ranges from 0 to 30
# Bottom edge midpoint is at (0, 0) in the front face coordinate system

sketch = front_wp.sketch()

# Draw a semicircle with radius 20mm
# Arc from (-20, 0) to (20, 0) curving upward
sketch.arc((-20.0, 0.0), (20.0, 0.0), 20.0)
# Close the profile with a line along the diameter
sketch.line((20.0, 0.0), (-20.0, 0.0))

sketch = sketch.finalize()

# Create the semicircular recess by cutting through the thickness
result = block.cutBlind(sketch, depth=20.0, direction=(-1, 0, 0))
