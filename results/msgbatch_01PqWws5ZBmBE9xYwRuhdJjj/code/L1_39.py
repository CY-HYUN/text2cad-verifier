import cadquery as cq
import math

# Create a new workplane with XY plane as the base
wp = cq.Workplane("XY")

# Draw the outer contour on the XY plane
# Rectangle: 60mm length (X), 40mm width (Y)
# Semicircle at the right side with diameter 40mm

# Start the sketch on the XY plane
sketch = wp.sketch()

# Draw the rectangle (60mm x 40mm)
# Corners: (0,0), (60,0), (60,40), (0,40)
# We'll draw from origin

# Draw left side (vertical line from bottom-left to top-left)
sketch = sketch.segment((0, 0), (0, 40))

# Draw top side (horizontal line from top-left to where semicircle starts)
sketch = sketch.segment((0, 40), (60, 40))

# Draw the semicircle at the right side
# The semicircle has diameter 40mm, so radius is 20mm
# Center of semicircle is at (60, 20) - midpoint of right side
# The semicircle extends from (60, 40) to (60, 0)
# Using arc: startPoint, endPoint, radius
# Arc from top-right (60, 40) to bottom-right (60, 0) with center at (60, 20)
sketch = sketch.arc((60, 40), (60, 0), radius=20, forceRadius=True)

# Draw bottom side (horizontal line from bottom-right back to origin)
sketch = sketch.segment((60, 0), (0, 0))

# Close the sketch
sketch = sketch.close()

# Create a face from the sketch
face = sketch.finalize().faces(">Z").workplane(offset=0)

# Extrude 10mm in the Z direction
result = face.extrude(10.0)
