import cadquery as cq
import math

# Create a workplane on the XZ plane and draw the frustum section profile
wp = cq.Workplane('XZ')

# Draw the frustum section profile on XZ plane:
# Outer radius transitions from 35 at Z=0 to 20 at Z=60
# Inner hole radius is 10 throughout
sketch = (wp
    .sketch()
    .moveTo(35.0, 0)      # Start at outer bottom (R=35, Z=0)
    .lineTo(20.0, 60.0)   # Outer edge to (R=20, Z=60)
    .lineTo(10.0, 60.0)   # Inner edge at top (R=10, Z=60)
    .lineTo(10.0, 0)      # Inner edge down (R=10, Z=0)
    .close()              # Close the section
    .finalize())

# Revolve 360° around Z-axis to create hollow frustum
result = sketch.revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 60))

# Apply 45° chamfer to the outer bottom edge (where R=35 meets Z=0)
result = result.edges("<<Z and >X").chamfer(2.0, 45)
