import cadquery as cq
import math

# Create a workplane on the XY plane and switch to XZ for sketching
wp = cq.Workplane("front")

# Create a sketch on the XZ plane
sketch = wp.sketch()

# Draw the profile in the XZ plane (X = radius, Z = axial)
# Start from bottom inner radius, go out, up with step and fillet, back in at top, down to start
sketch.move(12.5, 0)
sketch.line(20.0 - 12.5, 0)        # Outer radius at bottom: to (20.0, 0)
sketch.line(0, 60.0 - 3.0)         # Up to fillet point: to (20.0, 56.0)
sketch.arc((20.0, 60.0 + 3.0), 3.0)  # 3mm fillet at step
sketch.line(0, 120.0 - 63.0)       # Up to top: to (20.0, 120.0)
sketch.line(12.5 - 20.0, 0)        # Inward at top: to (12.5, 120.0)
sketch.line(0, -120.0)             # Down to start: to (12.5, 0)
sketch.close()

# Finalize sketch
sketch = sketch.finalize()

# Create the revolved solid
# Revolve around the Z-axis (vertical) to create the shaft sleeve
result = sketch.revolve(360, (0, 0, 1), (0, 0, 0))
