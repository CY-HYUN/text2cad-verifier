import cadquery as cq
import math

# Create the blank: 80x80 square base extruded by 45
base = cq.Workplane("XY").rect(80.0, 80.0).extrude(45.0)

# Create frustum by tapering from 80x80 to 50x50 over 45mm height
# Calculate taper angle
taper_angle = math.atan2((80.0 - 50.0) / 2.0, 45.0) * 180.0 / math.pi

# Build the frustum shape
frustum = cq.Workplane("XY").rect(80.0, 80.0).extrude(45.0, taper=taper_angle)

# Create the cavity: 30x30 square, 15mm deep from top
# First get the top face and create cavity sketch
cavity_workplane = frustum.faces(">Z").workplane()
cavity_sketch = cavity_workplane.rect(30.0, 30.0)

# Extrude the cavity downward (blind hole)
cavity = cavity_sketch.extrude(-15.0, combine=False)

# Cut the cavity from the frustum
result = frustum.cut(cq.Workplane("XY").workplane(offset=45.0).rect(30.0, 30.0).extrude(-15.0))

# Apply chamfer to the cavity opening edges
# Find edges at the top surface that form the cavity opening
result = result.edges(">Z").edges("<Z").chamfer(1.0)

