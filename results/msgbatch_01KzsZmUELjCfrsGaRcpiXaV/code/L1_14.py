import cadquery as cq
import math

# Create the cylinder base
cylinder = cq.Workplane("XY").cylinder(height=20, radius=25, centered=False)

# Create the cone on top using a solid created from a face
# Start with a circle at the top of the cylinder (z=20) and taper to a point at z=60
cone_sketch = cq.Workplane("XY").workplane(offset=20).circle(25).extrude(40, taper=-1)

# Combine the cylinder and cone
result = cylinder.union(cone_sketch)
