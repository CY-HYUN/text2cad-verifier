import cadquery as cq
import math

# Start with XZ plane sketch
sketch = cq.Sketch().on('XZ')

# Draw the frustum section profile:
# Outer radius transitions from 35 at Z=0 to 20 at Z=60
# Inner hole radius is 10 throughout

# Start at bottom outer radius (35, 0)
sketch = sketch.moveTo(35.0, 0)

# Draw outer edge from Z=0 to Z=60 (linear transition from R=35 to R=20)
sketch = sketch.lineTo(20.0, 60.0)

# Draw inner edge back down (R=10 throughout)
sketch = sketch.lineTo(10.0, 60.0)

# Close the profile by drawing back to start
sketch = sketch.lineTo(10.0, 0)
sketch = sketch.close()

# Create the workplane and apply the sketch
wp = cq.Workplane('XZ').planeData(cq.PlaneType.XZ)
face = sketch.face()

# Revolve around Z-axis (360 degrees) to create hollow frustum
result = cq.Workplane('XZ').revolve(360, axisEnd=(0, 0, 60), axisStart=(0, 0, 0))

# Start fresh with proper revolution
result = (cq.Workplane('XZ')
          .sketch()
          .moveTo(35.0, 0)
          .lineTo(20.0, 60.0)
          .lineTo(10.0, 60.0)
          .lineTo(10.0, 0)
          .close()
          .finalize()
          .revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 60)))

# Apply 45° chamfer to the outer bottom edge
# The outer bottom edge is where the outer radius (35) meets Z=0
result = result.edges("<<Z and >X").chamfer(2.0, 45)

