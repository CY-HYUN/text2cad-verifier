import cadquery as cq
import math

# Create a new part with units in millimeters
# Start with the base square (60mm x 60mm) on the XY plane
base_square = cq.Workplane("XY").rect(60.0, 60.0).extrude(0.1)

# Create the bottom face (60mm square at z=0)
bottom_face = cq.Workplane("XY").rect(60.0, 60.0)

# Create the top face (40mm square at z=30)
top_face = cq.Workplane("XY").offset(30.0).rect(40.0, 40.0)

# Create a frustum by lofting between bottom and top faces
# First, create sketches for lofting
bottom_sketch = cq.Workplane("XY").rect(60.0, 60.0).extrude(0.01)
top_sketch = cq.Workplane("XY").workplane(offset=30.0).rect(40.0, 40.0).extrude(0.01)

# Use a different approach: create the frustum using two squares and loft
# Create bottom square profile
bottom = cq.Workplane("XY").rect(60.0, 60.0)
# Create top square profile at height 30mm
top = cq.Workplane("XY").workplane(offset=30.0).rect(40.0, 40.0)

# Create frustum by lofting
frustum = bottom.loft([bottom, top], ruled=False)

# Now add the circular hole on the top face
# Create a hole at the top center (diameter 20mm)
result = (
    cq.Workplane("XY")
    .rect(60.0, 60.0)
    .loft([
        cq.Workplane("XY").rect(60.0, 60.0),
        cq.Workplane("XY").workplane(offset=30.0).rect(40.0, 40.0)
    ], ruled=False)
    .faces("+Z")
    .workplane()
    .hole(20.0, depth=30.0)
)
