import cadquery as cq
import math

# Start with a new workplane at the origin
wp = cq.Workplane("XY")

# Create a rectangle (60mm long x 20mm thick) and extrude it 30mm upward
block = wp.rect(60.0, 20.0).extrude(30.0)

# Now create a sketch on the front face (the face at y = 10, which is the front)
# Select the front face of the block
front_face = block.faces(">Y").first()

# Create a new workplane on the front face
front_wp = cq.Workplane("XY").workplaneFromFace(front_face)

# On this front face, we need to draw a semicircle centered at the midpoint of the bottom edge
# The bottom edge of the front face is at z=0, x goes from -30 to 30
# Center of bottom edge is at x=0, z=0

# Create a sketch on the front face
sketch = front_wp.sketch()

# Draw a semicircle with radius 20mm centered at (0, 0) on the front face
# The semicircle should curve upward (in the +Z direction)
# We'll create it by drawing an arc from (-20, 0) to (20, 0) with a bulge upward

# Using the arc method: arc((x1,y1), (x2,y2), radius)
# Or we can use a half-circle arc
# Center at origin, radius 20, from -20 to +20 on the horizontal axis

# Create the semicircular profile
sketch.arc((-20.0, 0.0), (20.0, 0.0), 20.0)  # Semicircle arc
sketch.line((20.0, 0.0), (-20.0, 0.0))  # Close the profile with a line

# Finalize the sketch
sketch = sketch.finalize()

# Perform an extruded cut through the entire thickness (20mm)
result = block.cutBlind(sketch, depth=20.0, direction=(-1, 0, 0))
