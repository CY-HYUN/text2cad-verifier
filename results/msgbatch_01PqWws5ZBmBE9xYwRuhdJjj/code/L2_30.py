import cadquery as cq
import math

# Create the initial rectangular prism
result = cq.Workplane("XY").box(60, 30, 30)

# First cut: Semi-elliptical arch at the bottom
# Select the front face and create a semi-elliptical sketch at the bottom center
result = result.faces("<Z").workplane().center(0, 0)

# Create semi-elliptical sketch on the front face for the arched bottom
# The semi-ellipse will be at the bottom edge, cutting through to the back
sketch1 = (
    cq.Workplane("XZ")
    .center(0, -15)  # Move to bottom edge of the front face
    .sketch()
    .arc((0, 0), (30, 0), (15, -10), forConstruction=False)  # Semi-ellipse: width 30mm, depth 10mm
    .finalize()
)

result = result.cut(cq.Workplane("XZ").transformed(offset=(0, -15, 0)).rect(60, 20).extrude(-30, both=False))

# Simpler approach: Cut a semi-cylindrical groove at the bottom
result = (
    cq.Workplane("XY")
    .box(60, 30, 30)
    .faces("<Z")
    .workplane()
    .sketch()
    .ellipse(30, 10)
    .finalize()
    .cutBlind(-10)
)

# Second cut: Circular hole from the top center going down
result = (
    result
    .faces(">Z")
    .workplane()
    .sketch()
    .circle(8)
    .finalize()
    .cutThruAll()
)
